from .reporter import download_data, save_data
import argparse


def main():
    parser = argparse.ArgumentParser(description='Calculate revenues and costs')
    parser.add_argument('--input_file', type=str, required=True, help='Input file')
    parser.add_argument('--output_file', type=str, required=True, help='Output file')

    args = parser.parse_args()
    data = download_data(args.input_file)

    grouped_df = data.groupby('category')['amount'].sum().reset_index()


    save_data(args.output_file, grouped_df)
    print('Данные сохранены по адресу: ', args.output_file)


if __name__ == '__main__':
    main()
