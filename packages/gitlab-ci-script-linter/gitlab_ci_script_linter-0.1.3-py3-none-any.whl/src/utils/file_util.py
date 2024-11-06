'''
Created on 01-07-2024

@author: Sydney
'''

import os
import re
from typing import Dict, List

from src.utils import ignore_keys, yml_util


def write_script_files(
        result: Dict,
        file_location: str,
        default_shebang: str,
        include_sast: bool,
        debug: bool) -> Dict:
    """Loop through the expanded yml and extract scripts to files"""
    expanded_ci = yml_util.load_yml_string(result.get("merged_yaml"))

    paths = {}

    for name, job in expanded_ci.items():

        # Tossing out all hidden keys, as if they are extended the script is included in the expanded job yml
        if not ignore_keys.should_parse_key(name, include_sast):
            continue

        before = []
        script = []
        after = []

        if "before_script" in job:
            before = job["before_script"]

        if "script" in job:
            script = job["script"]

        if "after_script" in job:
            after = job["after_script"]

        shebang = find_shebang(before, script, after)
        if not shebang:
            shebang = "#!" + default_shebang

        filenames = write_file(name, before, script, after, file_location, shebang, debug)
        paths[name] = filenames

    return paths

def write_file(
        name: str,
        before: List,
        script: List,
        after: List,
        file_location: str,
        shebang: str,
        debug: bool) -> List:
    """Write script files for a job"""
    files = []

    if not os.path.exists(file_location):
        os.makedirs(file_location)

    if before or script:
        file = file_location + "/" + to_kebab_case(name) + ".sh"
        if debug:
            print("Writing file for " + file)
        with open(file, "w", encoding="utf-8") as f:
            f.write(shebang + '\n')

            flatbefore = flatten_script(before, [])
            flat = flatten_script(script, flatbefore)
            for line in flat:
                f.write(line + '\n')
        if debug:
            print(file)
        files.append(file)

    if after:
        afterfile = file_location + "/" + to_kebab_case(name) + "_after.sh"
        if debug:
            print("Writing file for " + afterfile)
        with open(afterfile, "w", encoding="utf-8") as f:
            f.write(shebang + '\n')
            flatafter = flatten_script(after, [])
            for line in flatafter:
                f.write(line + '\n')
        if debug:
            print(afterfile)
        files.append(afterfile)

    return files

def find_shebang(
        before: List,
        script: List,
        after: List) -> str | None:
    """Attempt to extract shebang from the script sections"""

    flatbefore = flatten_script(before, [])
    if flatbefore and flatbefore[0].startswith("#!"):
        return flatbefore[0]

    flatscript = flatten_script(script, [])
    if flatscript and flatscript[0].startswith("#!"):
        return flatscript[0]

    flatafter = flatten_script(after, [])
    if flatafter and flatafter[0].startswith("#!"):
        return flatafter[0]

    return None

def to_kebab_case(value: str) -> str:
    """Modify job name to kebab case for file names"""
    return "-".join(re.split(r'[_\s]', value.lower()))

def flatten_script(
        script: List,
        flatscript: List
        ) -> List:
    """If scripts are built using !reference the injected sections become sublists."""

    for element in script:
        if isinstance(element, list):
            flatten_script(element, flatscript)
        else:
            flatscript.append(element)

    return flatscript
