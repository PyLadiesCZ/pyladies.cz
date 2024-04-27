import os
import sys
import importlib.util

import pytest

def register_app_as_module():
    """ Registers the pyladies_cz.py script file as a module so we can use it
    for testing. """
    spec = importlib.util.spec_from_file_location("pyladies_cz", "pyladies_cz.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["pyladies_cz"] = module
    spec.loader.exec_module(module)

register_app_as_module()

import pyladies_cz

def test_read_yaml():
    """ Test of reading a yaml file. """
    root_path = os.path.dirname(os.path.realpath(__file__))
    yaml_file_path = f"{root_path}/mock_data/yaml/valid.yaml"
    yaml = pyladies_cz.read_yaml(yaml_file_path)

    assert yaml
    assert type(yaml) is list
    assert len(yaml) == 4


def test_read_yaml_bad_format():
    """
    Test for yaml file reading failure. Checks if the thrown exception is
    the correct one an has appropriate message with all necessary information.
    """
    root_path = os.path.dirname(os.path.realpath(__file__))
    yaml_file_path = f"{root_path}/mock_data/yaml/invalid.yaml"

    with pytest.raises(pyladies_cz.YamlIOException) as e:
        pyladies_cz.read_yaml(yaml_file_path)

    assert "can not be read" in e.value.args[0]
    assert yaml_file_path in e.value.args[0]
