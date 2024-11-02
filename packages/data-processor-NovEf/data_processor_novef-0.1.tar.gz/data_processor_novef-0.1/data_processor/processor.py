import pandas as pd
import csv


def download_data(file_path):
    return pd.read_csv(file_path)

def save_data(file_path, grouped):
    with open(file_path, 'w', newline='') as file:
        fieldnames=['category', 'sales', 'quantity']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(grouped)