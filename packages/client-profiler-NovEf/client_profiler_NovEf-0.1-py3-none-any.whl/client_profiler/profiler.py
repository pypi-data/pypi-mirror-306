import pandas as pd

def download_data(file_path):
    return pd.read_csv(file_path)

def distribution_by_age(df):
    labels = ['0-17', '18-25', '26-35', '36-45', '46-60', '61+']
    bins = [0, 17, 25, 35, 45, 60, float('inf')]
    df['AgeGroup'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)
    grouped = df.groupby('AgeGroup', observed=False)['customer_id'].count()
    return grouped

def distribution_by_cities(df):
    return df.groupby('city')['customer_id'].count()

def total_clients(df):
    return len(df)

def save_data(file_path, ages, clients, towns):
    with open(file_path, 'w') as file:
        file.write(f'Общее количество клиентов: {clients}\n\n')
        file.write(f'Количество клиентов по возрастным группам:\n')
        file.write(ages.reset_index().apply(lambda row: f"{row['AgeGroup']}: {row['customer_id']}", axis=1).to_csv(
            index=False,
            header=False,
            sep='\t'))
        file.write(f'\n')
        file.write(f'Разделение клиентов по городам:\n')
        file.write(towns.reset_index().apply(lambda row: f"{row['city']}: {row['customer_id']}", axis=1).to_csv(
            index=False,
            header=False,
            sep='\t'))
        file.write(f'\n')