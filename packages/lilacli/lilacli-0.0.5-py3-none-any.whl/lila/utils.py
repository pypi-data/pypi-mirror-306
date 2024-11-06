import os
import re


def replace_env_vars(content: str) -> str:
    # Searches for all ${VAR_NAME} and replaces them with the value of the environment variable VAR_NAME
    regex = re.compile(r"\${(.*?)}")
    for match in regex.findall(content):
        value = os.environ.get(match)
        if value is None:
            continue
        content = content.replace(f"${{{match}}}", value)

    return content
