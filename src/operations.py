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
