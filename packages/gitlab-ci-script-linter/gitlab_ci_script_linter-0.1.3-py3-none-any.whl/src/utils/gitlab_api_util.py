'''
Created on 28-06-2024

@author: Sydney
'''
from argparse import Namespace
from typing import Dict

import requests

from src.utils import yml_util


def validate_ci_file(
    args: Namespace,
    branch: str
) -> Dict:
    """Validate file and return the result"""

    escaped_file = yml_util.read_yaml_file(args.file)

    gitlab_headers = {"Authorization": "Bearer " + args.token}
    gitlab_api_url = (
        args.url + "/projects/" + args.projectid + "/ci/lint")

    if branch is None:
        payload = {"content": escaped_file}
    else:
        payload = {"content": escaped_file, "dry_run": True, "ref": branch}

    response = requests.post(gitlab_api_url, json = payload, headers=gitlab_headers, timeout=30)

    return response.json()
