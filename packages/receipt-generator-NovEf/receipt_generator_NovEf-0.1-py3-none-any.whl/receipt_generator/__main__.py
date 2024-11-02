from .generator import download_data, save_data, list_of_items
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description='Analyzing data')
    parser.add_argument('--input_file', type=str, required=True, help='Input file')
    parser.add_argument('--output_file', type=str, required=True, help='Output file')

    args = parser.parse_args()
    data = download_data(args.input_file)

    items = list_of_items(data)
    df = pd.DataFrame(items)
    df.rename(columns={
        'name': 'Наименование товара',
        'quantity': 'Количество',
        'price': 'Цена за товар'
    }, inplace=True)
    customer_name = data['customer_name']

    save_data(args.output_file, df, customer_name)
    print('Данные сохранены по адресу: ', args.output_file)


if __name__ == '__main__':
    main()
