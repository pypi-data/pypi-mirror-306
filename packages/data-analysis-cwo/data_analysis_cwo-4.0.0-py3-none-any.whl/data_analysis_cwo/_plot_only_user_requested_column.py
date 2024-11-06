
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_csv(file_path):
    return pd.read_csv(file_path)

def plot_data(data, x_column, y_column, log_x=False, log_y=False):
    plt.figure(figsize=(10, 6))

    x_data = data[x_column]
    y_data = data[y_column]

    if log_x:
        x_data = np.log(np.abs(x_data))
    if log_y:
        y_data = np.log(np.abs(y_data))

    plt.plot(x_data, y_data, marker='o', linestyle='-')

    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Plot of {y_column} vs {x_column}')

    if log_x:
        plt.xlabel(f'Log(|{x_column}|)')
    if log_y:
        plt.ylabel(f'Log(|{y_column}|)')

    plt.grid(True)
    plt.show()
def _plot_only_user_requested_column():
    # User inputs
    file_path = input("Enter the path to the CSV file: ")
    data = read_csv(file_path)

    print("Available columns:")
    print(data.columns)

    x_column = input("Enter the column name for the x-axis: ")
    y_column = input("Enter the column name for the y-axis: ")

    log_x = input("Apply logarithmic filter to x-axis? (yes/no): ").lower() == 'yes'
    log_y = input("Apply logarithmic filter to y-axis? (yes/no): ").lower() == 'yes'

    plot_data(data, x_column, y_column, log_x, log_y)

