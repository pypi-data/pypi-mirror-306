from .profiler import download_data, save_data, distribution_by_age, total_clients, distribution_by_cities
import argparse


def main():
    parser = argparse.ArgumentParser(description='Data Profiler')
    parser.add_argument('--input_file', type=str, required=True, help='Input file')
    parser.add_argument('--output_file', type=str, required=True, help='Output file')

    args = parser.parse_args()
    df = download_data(args.input_file)

    ages = distribution_by_age(df)
    clients = total_clients(df)
    towns = distribution_by_cities(df)

    save_data(args.output_file, ages, clients, towns)
    print('Данные сохранены по адресу: ', args.output_file)


if __name__ == '__main__':
    main()
