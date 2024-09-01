import pytest
from json import load
import os


@pytest.fixture
def data_json():

    default_dict = {}

    with open(os.path.abspath("src/operations_account.json"), encoding='utf-8') as json_file:
        data_operations = load(json_file)

    for data_operation in data_operations:
        default_dict['id'] = data_operation['id']
        default_dict['state'] = data_operation['state']
        default_dict['date'] = data_operation['date']
        default_dict['description'] = data_operation['description']
        default_dict['from'] = data_operation['from']
        default_dict['to'] = data_operation['to']
        break

    return default_dict
