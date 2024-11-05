'''
Created on 28-06-2024

@author: Sydney
'''

import io
import logging
import logging.config
import os.path
from typing import Dict

from ruamel.yaml import YAML

from src.core.log_config import LOGGING_CONFIG
from src.exception.file_exception import FileException

# Setup logger
logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger(__name__)

def read_yaml_file(file_path: str) -> str:
    """Read a yaml file and produce an escaped string"""

    if not os.path.exists(file_path):
        raise FileException("File does not exist", file_path)

    yaml = YAML()
    yaml.preserve_quotes = True

    with open(file_path, 'r', encoding="utf-8") as file:
        try:
            f = io.StringIO()
            yaml_content = yaml.load(file)
            yaml.dump(yaml_content, f)
            f.seek(0)
            return f.read()
        except Exception as e:
            log.exception("Error reading YAML file:")
            raise e

def load_yml_string(escaped_string: str) -> Dict:
    """Read an escaped yml string and produce a Dict"""

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        return yaml.load(escaped_string)
    except Exception as e:
        log.exception("Error loading escaped yml string:")
        raise e
