'''
Created on 28-06-2024

@author: Sydney
'''

import logging
import logging.config
import os
import subprocess
import sys

from src.core.arg_parser import LintArgParse
from src.core.log_config import LOGGING_CONFIG
from src.utils import file_util, gitlab_api_util

SYSTEM_ENV = dict(os.environ)

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger(__name__)

parser = LintArgParse().configure(SYSTEM_ENV)
args = parser.parse_args()

branch = None
if hasattr(args, 'branch') and args.branch:
    branch = args.branch

try:
    result = gitlab_api_util.validate_ci_file(args, branch)
except Exception as e:
    log.exception(e)
    sys.exit(1)

print("CI is valid: " + str(result.get("valid")))
if not result.get("valid"):
    print("Found errors: " + str(result.get("errors")))
    print("Found warnings: " + str(result.get("warnings")))
    sys.exit(1)

files = file_util.write_script_files(result, args.output, args.shell, args.sast, args.debug)
returncode = 0 # pylint: disable=C0103

for name, paths in files.items():
    print(f"\033[96m{name}: \033[00m")
    for path in paths:
        if args.debug:
            with open(path, 'r', encoding="utf-8") as f:
                print(f.read())
        lint = subprocess.run(["shellcheck", "--format=tty", "--color=always", "-S", args.severity, path], capture_output=True, text=True, check=False)
        print(lint.stdout)
        if lint.returncode != 0:
            returncode = lint.returncode
            print("Shellcheck gave return code: " + str(lint.returncode))
        else:
            print("No errors found")

sys.exit(returncode)
