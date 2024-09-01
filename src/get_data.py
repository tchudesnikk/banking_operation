from datetime import datetime
from io import open
from json import load
import os
from operations import Operation


def get_formatted_date(date: str, format_date: str):
    """ Форматируем дату из в строки в тип DateType """

    return datetime.strptime(date[0:10], format_date)


def get_hide_numbers(value: str):
    """ Делает в строке все символы скрытыми
    Возвращает строку"""

    hide_string = ''

    for i in value:
        hide_string += i.replace(i, '*')

    return hide_string


def card_number_mask(info_bank_account: str):
    """ Маскирует данные карты и счета по шаблону: Номер карты - XXXX XX** **** XXXX
    Номер счета - ***************XXXX для безопасности
    Возвращает кортеж данных: Имя счета, оригинальный счет, замаскированный счет"""

    list_info_account = info_bank_account.split(" ")
    number_account = list_info_account[-1]
    list_info_account.pop(-1)

    if list_info_account[0].lower() == 'счет':
        number_account_mask = f'{get_hide_numbers(number_account[:-4])}{number_account[-4:]}'
    else:
        number_account_mask = f"{number_account[0:4]} {number_account[4:6]}** **** {number_account[-4:]}"

    return ''.join(list_info_account),number_account,number_account_mask


def get_data_from_json():
    """ Получает данные из JSON и возвращает список классов """
    operations = []

    with open(os.path.abspath("operations_account.json"), encoding='utf-8') as json_file:
        data_operations = load(json_file)

    for data_operation in data_operations:

        try:
            operation = Operation(data_operation['id'],
                                  data_operation['state'],
                                  get_formatted_date(data_operation['date'], "%Y-%m-%d"),
                                  data_operation['operationAmount']['amount'],
                                  data_operation['operationAmount']['currency']['name'])
        except KeyError:
            continue

        if 'description' in data_operation.keys():
            operation.add_description(data_operation['description'])

        if 'from' in data_operation.keys():
            info_bank_account = card_number_mask(data_operation['from'])
            operation.add_sender(info_bank_account[0], info_bank_account[1], info_bank_account[2])

        if 'to' in data_operation.keys():
            info_bank_account = card_number_mask(data_operation['to'])
            operation.add_recipient(info_bank_account[0], info_bank_account[1], info_bank_account[2])

        operations.append(operation)

    return operations
