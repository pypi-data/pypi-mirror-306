import os
import sys
import click
import requests
from typing import TextIO, Dict
from halo import Halo
from tenacity import retry, stop_after_delay, wait_fixed, retry_if_exception_type
import yaml
from concurrent.futures import ThreadPoolExecutor


from lila.utils import replace_env_vars


BASE_URL = 'https://app.lila.dev'
TIMEOUT = 10 * 60  # 10 minutes
MAX_CONCURRENT_TESTS = 2


def raise_for_status(response: requests.Response):
    try:
        response.raise_for_status()
    except requests.RequestException as e:
        data = response.json()
        raise RuntimeError(f"Error: {data}") from e


@retry(stop=stop_after_delay(TIMEOUT),
       wait=wait_fixed(5),
       retry=(retry_if_exception_type(requests.RequestException) |
              retry_if_exception_type(RuntimeError)))
def wait_test(test_id: str) -> Dict:
    response = requests.get(
        f'{BASE_URL}/api/v1/testcases/{test_id}',
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {os.environ['LILA_API_KEY']}"
        }
    )
    raise_for_status(response)
    if response.status_code == 286:
        return response.json()['testcase']

    raise RuntimeError(f"Test case still running.")


def post_test(content: str) -> Dict:
    if 'LILA_API_KEY' not in os.environ:
        raise RuntimeError("LILA_API_KEY environment variable must be set")

    content = replace_env_vars(content)

    response = requests.post(
        f'{BASE_URL}/api/v1/testcases',
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Authorization": f"Bearer {os.environ['LILA_API_KEY']}",
            "HX-Lila-Client": "lila-cli"
        },
        data={
            "test_content": content
        }
    )
    raise_for_status(response)
    if response.status_code == 202:
        return response.json()["testcase"]

    raise requests.RequestException(f"Unexpected status code: {response.status_code}")


def get_report(test_id: str) -> Dict:
    response = requests.get(
        f'{BASE_URL}/api/v1/testcases/{test_id}/report',
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {os.environ['LILA_API_KEY']}"
        }
    )
    raise_for_status(response)

    if response.status_code == 200:
        return response.json()["report"]

    raise requests.RequestException(f"Unexpected status code: {response.status_code}")

def print_report(report: Dict, testcase_run: Dict, content: str, testfile_name: str):
    content = yaml.safe_load(content)
    if testcase_run['conclusion'] == 'success':
        click.secho(f"Test {testfile_name} passed. View the report at {BASE_URL}/runs/{testcase_run['id']}", fg='green')
    else:
        click.secho(f"Test {testfile_name} failed. View the report at {BASE_URL}/runs/{testcase_run['id']}", fg='red')
        click.echo()
        for idx, url in enumerate(report):
            steps = report[url]

            click.secho(f"\tURL: {url}")
            for step in steps:
                step_content = content['case'][idx]['steps'][step['step_number']]
                if step['success']:
                    click.secho(f"\t\tPASSED: {step_content}", fg='green')
                else:
                    click.secho(f"\t\tFAILED: {step_content}: {step['msg']}", fg='red')
    click.echo()

def enable_spinner():
    CI_ENVS = [
        'GITHUB_ACTIONS'
    ]
    for env in CI_ENVS:
        if os.environ.get(env):
            return False

    return True


def run_test_file(content: str, test_file: str) -> Dict:
    testcase = post_test(content)
    click.echo(f"Started test {test_file} with id {testcase['id']}")
    testcase_run = wait_test(testcase['id'])
    return testcase_run



@click.command()
@click.option('--test-file', type=click.File('r'))
@click.option('--test-dir', type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True))
def run(test_file, test_dir):
    click.secho("Lila running tests", fg='blue')
    click.echo()
    if test_file:
        content = test_file.read()
        testcase_run = run_test_file(content, test_file.name)
        report = get_report(testcase_run['id'])
        print_report(report, testcase_run, content, test_file.name)
        if testcase_run['conclusion'] == 'failure':
            # Fail with a non-zero exit code if the test failed
            return sys.exit(1)
        return sys.exit(0)

    if test_dir:
        exit_code = 0
        # Run all test files in the directory
        # In parallel
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_TESTS) as executor:
            futures = []
            for test_file in os.listdir(test_dir):
                if test_file.endswith('.yaml'):
                    with open(os.path.join(test_dir, test_file)) as f:
                        content = f.read()
                        futures.append(executor.submit(run_test_file, content, test_file))

            for future in futures:
                testcase_run = future.result()
                report = get_report(testcase_run['id'])
                print_report(report, testcase_run, content, test_file)
                if testcase_run['conclusion'] == 'failure':
                    exit_code = 1

        return sys.exit(exit_code)

    raise click.UsageError("Either --test-file or --test-dir must be provided")
