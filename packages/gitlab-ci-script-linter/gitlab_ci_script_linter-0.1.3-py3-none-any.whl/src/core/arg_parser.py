'''
Exception raised for file read errors

@author: Sydney
'''
import argparse


class LintArgParse(argparse.ArgumentParser):
    """Exception raised for file read errors"""

    def __init__(self):
        super().__init__()

    def configure(self, system_env: dict) -> argparse.ArgumentParser:
        """Validate file and return the result"""

        parser = argparse.ArgumentParser(
            description="Collate .gitlab-ci.yml files into script sections for linting"
        )
        parser.add_argument(
            "-v", "--version", action="version", version=f"{parser.prog} version 0.1.0"
        )
        parser.add_argument(
            "-t", "--token",
            help="API Token with permissions to call CI Lint API",
            required=True
        )
        parser.add_argument(
            "-b", "--branch",
            help="Git branch/tag, if this is set a dry run will be done against this branch",
        )
        parser.add_argument(
            "-o", "--output",
            help="Directory in which to write expanded scripts (Default: scripts)",
            default="scripts"
        )
        parser.add_argument(
            "-p", "--projectid",
            help="ID of the Gitlab project (Default $CI_PROJECT_ID)",
            default=system_env.get("CI_PROJECT_ID")
        )
        
        parser.add_argument(
            "-e", "--severity",
            help="Minimum serverity of errors to consider for shellcheck run (Default: warning)",
            default="warning"
        )
        parser.add_argument(
            "-s", "--shell",
            help="Default path to be used when adding shebang to script file (Default: /bin/sh)",
            default="/bin/sh"
        )
        parser.add_argument(
            "-u", "--url",
            help="Gitlab API URL (Default $CI_API_V4_URL)",
            default=system_env.get("CI_API_V4_URL")
        )
        parser.add_argument(
            "--debug",
            help="Enable debug output, primarily printing script files",
            action="store_true",
            default=False
        )
        parser.add_argument(
            "--sast",
            help="Indicate if Gitlab SAST jobs should be scanned. False if not present",
            action="store_true",
            default=False
        )
        parser.add_argument(
            "file", nargs="?",
            default=".gitlab-ci.yml",
            help="CI file that you want to lint (Default .gitlab-ci.yml)"
        )
        return parser
