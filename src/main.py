from get_data import get_data_from_json


def delete_canceled_operation():
    for i in range(len(operations)-1, -1, -1):
        if operations[i].state.upper() == "CANCELED":
            operations.pop(i)


def sorted_operation():
    return sorted(operations, key=lambda operation: operation.date)[0:5]


operations = get_data_from_json()
delete_canceled_operation()
successful_transactions = sorted_operation()
for operation in successful_transactions:
    print(operation)
