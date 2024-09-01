from get_data import get_data_from_json

operations = get_data_from_json()

for i in range(len(operations)-1, -1, -1):
    if operations[i].state.upper() == "CANCELED":
        operations.pop(i)

for operation in sorted(operations, key=lambda operation: operation.date)[0:5]:
    print(operation)
