import os
import sys
import importlib.util

import pytest

import pyladies_cz

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


def test_read_yaml():
    """ Test of reading a yaml file. """
    yaml_file_path = f"{ROOT_PATH}/mock_data/yaml/valid.yaml"
    yaml = pyladies_cz.read_yaml(yaml_file_path)

    assert yaml
    assert type(yaml) is list
    assert len(yaml) == 4


def test_read_yaml_bad_format():
    """
    Test for yaml file reading failure. Checks if the thrown exception is
    the correct one an has appropriate message with all necessary information.
    """
    yaml_file_path = f"{ROOT_PATH}/mock_data/yaml/invalid.yaml"

    with pytest.raises(pyladies_cz.YamlIOException) as e:
        pyladies_cz.read_yaml(yaml_file_path)

    assert "can not be read" in e.value.args[0]
    assert yaml_file_path in e.value.args[0]
