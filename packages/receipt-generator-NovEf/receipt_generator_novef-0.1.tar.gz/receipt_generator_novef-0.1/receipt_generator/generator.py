import json


def download_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def list_of_items(data):
    items = data['items']
    data_for_df = {'name': [], 'quantity': [], 'price': []}
    for elem in items:
        data_for_df['name'].append(elem['name'])
        data_for_df['quantity'].append(elem['quantity'])
        data_for_df['price'].append(elem['price'])
    return data_for_df


def save_data(file_path, df, customer_name):
    total_sum = (df['Количество'] * df['Цена за товар']).sum()
    with open(file_path, 'w') as file:
        file.write(f'Имя клиента: {customer_name}\n\nСписок товаров:\n')
        file.write(f'{df}\nОбщая сумма заказа: {total_sum} руб')
