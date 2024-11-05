import os
import click
import requests
from typing import TextIO, Dict
from halo import Halo
from tenacity import retry, stop_after_delay, wait_fixed, retry_if_exception_type
import yaml

from lila.utils import replace_env_vars


BASE_URL = 'https://app.lila.dev'
TIMEOUT = 10 * 60  # 10 minutes


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
    response.raise_for_status()
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
            "Authorization": f"Bearer {os.environ['LILA_API_KEY']}"
        },
        data={
            "test_content": content
        }
    )
    response.raise_for_status()
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
    response.raise_for_status()

    if response.status_code == 200:
        return response.json()["report"]

    raise requests.RequestException(f"Unexpected status code: {response.status_code}")

def print_report(report: Dict, testcase_run: Dict, content: str, testfile_name: str):
    content = yaml.safe_load(content)
    if testcase_run['conclusion'] == 'success':
        click.secho(f"Test {testfile_name} passed", fg='green')
    else:
        click.secho(f"Test {testfile_name} failed", fg='red')
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
    try:
        testcase = post_test(content)
        with Halo(text=f'Running test {test_file}', spinner='dots', enabled=enable_spinner()) as spinner:
            testcase_run = wait_test(testcase['id'])
            if testcase_run["conclusion"] == "success":
                spinner.succeed()
            else:
                spinner.fail()

        return testcase_run
    except (requests.RequestException, RuntimeError) as e:
        click.UsageError(f"Error: {e}")


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
            raise click.Abort()

        return

#     if test_dir:
#         for root, dirs, files in os.walk(test_dir):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 with open(file_path, 'r') as f:
#                     run_test_file(f)
#         return

    raise click.UsageError("Either --test-file or --test-dir must be provided")
