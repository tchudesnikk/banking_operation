from datetime import datetime
from io import open
from json import load
import os


class Operation:
    """ Хранит данные по банковским операциям """

    def __init__(self, id_operation, state, date, amount, currency):
        self.id_operation = id_operation
        self.state = state
        self.date = date
        self.amount = amount
        self.currency = currency
        self.description = ''
        self.sender = ''
        self.sender_number_card = ''
        self.sender_number_card_mask = ''
        self.recipient = ''
        self.recipient_number_card = ''
        self.recipient_number_card_mask = ''

    def __repr__(self):
        """ Стандартизированный вывод по транзакции для пользователей """
        return f"""{self.date.date().strftime('%d.%m.%Y')} {self.description}
{self.sender} {self.sender_number_card_mask} -> {self.recipient} {self.recipient_number_card_mask}
{self.amount} {self.currency}\n"""

    def add_sender(self, sender, number_card, mask_number_card):
        """ Добавляет данные по отправителю """
        self.sender = sender
        self.sender_number_card = number_card
        self.sender_number_card_mask = mask_number_card

    def add_recipient(self, recipient, number_card, mask_number_card):
        """ Добавляет данные по получателю """
        self.recipient = recipient
        self.recipient_number_card = number_card
        self.recipient_number_card_mask = mask_number_card

    def add_description(self, description):
        """ Добавляет описание транзации"""
        self.description = description



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
    banking_operations = []

    with open(os.path.abspath("./config/operations_account.json"), encoding='utf-8') as json_file:
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

        banking_operations.append(operation)

    return banking_operations
