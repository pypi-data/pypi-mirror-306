from .processor import download_data, save_data
import argparse


def main():
    parser = argparse.ArgumentParser(description='Analyzing data')
    parser.add_argument('--input_file', type=str, required=True, help='Input file')
    parser.add_argument('--output_file', type=str, required=True, help='Output file')

    args = parser.parse_args()
    data = download_data(args.input_file)

    grouped_df = data.groupby('category')[['sales', 'quantity']].sum().reset_index()

    save_data(args.output_file, grouped_df.to_dict(orient='records'))
    print('Данные сохранены по адресу: ', args.output_file)


if __name__ == '__main__':
    main()
