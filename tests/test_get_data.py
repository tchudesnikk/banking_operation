from datetime import datetime

from src import get_data


def test_get_formatted_date():
    default_value = datetime.strptime("07-04-1995", "%d-%m-%Y")
    assert(get_data.get_formatted_date("1995-04-07T10:50:58.294041", "%Y-%m-%d")) == default_value

def test_get_hide_numbers():
    assert(get_data.get_hide_numbers("123456")) == "******"

def test_get_hide_numbers_empty():
    assert(get_data.get_hide_numbers("")) == ""

def test_card_number_mask():
    default_value = "Maestro 1596837868705199"
    name_card, origin_card_number, mask_card_number = get_data.card_number_mask(default_value)
    assert name_card == "Maestro"
    assert origin_card_number == "1596837868705199"
    assert mask_card_number == "1596 83** **** 5199"

def test_account_number_mask():
    default_value = "Счет 64686473678894779589"
    name_account, origin_account_number, mask_account_number = get_data.card_number_mask(default_value)
    assert name_account == "Счет"
    assert origin_account_number == "64686473678894779589"
    assert mask_account_number == "****************9589"

def test_get_data_from_json(data_json):
    operations = get_data.get_data_from_json()

    assert(len(operations)) > 1

    operation = operations[0]

    assert operation.id_operation == data_json['id']
    assert operation.state == data_json['state']
    assert operation.date == data_json['date']
    assert operation.description == data_json['description']
    assert f'{operation.sender} {operation.sender_number_card}' == data_json['from']
    assert f'{operation.recipient} {operation.recipient_number_card}' == data_json['to']
