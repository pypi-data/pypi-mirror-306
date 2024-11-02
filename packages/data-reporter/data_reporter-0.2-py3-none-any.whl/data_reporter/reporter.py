import pandas as pd


def download_data(file_path):
    return pd.read_csv(file_path)

def save_data(file_path, grouped):
    with open(file_path, 'w') as file:
        for  index, row in grouped.iterrows():
            file.write(f"{row['category']}:\t{row['amount']} руб.\n")