'''
Created on 02-07-2024

@author: Sydney
'''
global_keys = [
    "variables",
    "stages",
    "include",
    "workflow",
    "spec"
]

sast_keys = [
    "sast",
    "gitlab-advanced-sast",
    "bandit-sast",
    "brakeman-sast",
    "eslint-sast",
    "flawfinder-sast",
    "kubesec-sast",
    "gosec-sast",
    "mobsf-android-sast",
    "mobsf-ios-sast",
    "nodejs-scan-sast",
    "phpcs-security-audit-sast",
    "pmd-apex-sast",
    "security-code-scan-sast",
    "semgrep-sast",
    "sobelow-sast",
    "spotbugs-sast"
]

def should_parse_key(
        key: str,
        include_sast: bool
        ) -> bool:
    """Determine whether a key should be parsed"""
    if key.startswith("."):
        return False

    if key in global_keys:
        return False

    if not include_sast and key in sast_keys:
        return False

    return True
