import os
import time

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def read_csv(file_path):
    return pd.read_csv(file_path)


def plot_data(data, x_column, y_column, log_x=False, log_y=False, label=None):
    x_data = data[x_column]
    y_data = data[y_column]

    if log_x:
        x_data = np.log(np.abs(x_data))
    if log_y:
        y_data = np.log(np.abs(y_data))

    plt.plot(x_data, y_data, linestyle='-', label=label)


def list_subfolders(directory_path):
    subfolders = []
    for root, dirs, files in os.walk(directory_path):
        for dir in dirs:
            subfolders.append(os.path.relpath(os.path.join(root, dir), directory_path))
    return subfolders


def find_minima(data, x_column, y_column, log_x=False, log_y=False):
    x_data = data[x_column]
    y_data = data[y_column]

    if log_x:
        x_data = np.log(np.abs(x_data))
    if log_y:
        y_data = np.log(np.abs(y_data))

    positive_minima = []
    negative_minima = []

    for i in range(1, len(x_data) - 1):
        if y_data[i] < y_data[i - 1] and y_data[i] < y_data[i + 1]:
            if x_data[i] > 0:
                positive_minima.append((x_data[i], y_data[i]))
            else:
                negative_minima.append((x_data[i], y_data[i]))

    positive_minima.sort(key=lambda x: x[1])
    negative_minima.sort(key=lambda x: x[1])

    return positive_minima[:2], negative_minima[:2]


def plot_minima(data, x_column, y_column, positive_minima, negative_minima, log_x=False, log_y=False):
    x_data = data[x_column]
    y_data = data[y_column]

    if log_x:
        x_data = np.log(np.abs(x_data))
    if log_y:
        y_data = np.log(np.abs(y_data))

    plt.plot(x_data, y_data, linestyle='-')

    for x, y in positive_minima:
        plt.plot(x, y, 'ro')  # Red circle for positive minima
    for x, y in negative_minima:
        plt.plot(x, y, 'bo')  # Blue circle for negative minima

    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Plot of {y_column} vs {x_column} with Minima')

    if log_x:
        plt.xlabel(f'Log(|{x_column}|)')
    if log_y:
        plt.ylabel(f'Log(|{y_column}|)')

    plt.grid(True)
    plt.show()

def _plot_from_subfolders_until_user_terminate():
    global table_df
    directory_path = None
    subfolders = None
    selected_subfolders = None
    files = None

    while True:
        if directory_path is None:
            directory_path = input("Enter the path to the directory containing CSV files: ")

        if subfolders is None:
            subfolders = list_subfolders(directory_path)
            if not subfolders:
                print("No subfolders found in the directory.")
                continue

            subfolders.append("all")

            print("Available subfolders:")
            for i, subfolder in enumerate(subfolders):
                print(f"{i + 1}. {subfolder}")

            selected_subfolders = input(
                "Enter the numbers of the subfolders you want to plot (separated by spaces): ").split()
            selected_subfolders = [subfolders[int(num) - 1] for num in selected_subfolders]

        if files is None:
            files = []
            for subfolder in selected_subfolders:
                if subfolder == "all":
                    for root, _, filenames in os.walk(directory_path):
                        for filename in filenames:
                            if filename.endswith('.csv'):
                                files.append(os.path.join(root, filename))
                else:
                    subfolder_path = os.path.join(directory_path, subfolder)
                    for root, _, filenames in os.walk(subfolder_path):
                        for filename in filenames:
                            if filename.endswith('.csv'):
                                files.append(os.path.join(root, filename))

            if not files:
                print("No CSV files found in the selected subfolders.")
                continue

        print("Available CSV files:")
        for i, file in enumerate(files):
            print(f"{i + 1}. {file}")

        selected_files = input(
            "Enter the numbers of the files you want to plot (separated by spaces) or 'all' for all files: ").split()
        if 'all' in selected_files:
            selected_files = list(range(len(files)))
        else:
            selected_files = [int(num) - 1 for num in selected_files]

        same_plot = input("Do you want to plot all selected files on the same plot? (yes/no): ").lower() == 'yes'

        first_file_path = files[selected_files[0]]
        first_data = read_csv(first_file_path)
        print("Available columns:")
        print(first_data.columns)

        x_column = input("Enter the column name for the x-axis: ")
        y_column = input("Enter the column name for the y-axis: ")

        log_x = input("Apply logarithmic filter to x-axis? (yes/no): ").lower() == 'yes'
        log_y = input("Apply logarithmic filter to y-axis? (yes/no): ").lower() == 'yes'

        table_data = []
        if same_plot:
            plt.figure(figsize=(10, 6))
            all_positive_minima = []
            all_negative_minima = []
            for index in selected_files:

                file_path = files[index]
                data = read_csv(file_path)
                label_name = os.path.join(*file_path.split(os.sep)[-3:])

                positive_minima, negative_minima = find_minima(data, x_column, y_column, log_x, log_y)

                print(f"Minima Calculated from:{label_name}")
                print("Positive Minima:")
                for x, y in positive_minima:
                    print(f"({x}, {y})")

                print("Negative Minima:")
                for x, y in negative_minima:
                    print(f"({x}, {y})")

                if len(positive_minima) >= 2:
                    diff_positive = positive_minima[1][1] - positive_minima[0][1]
                    print(f"Difference between first two positive minima: {diff_positive}")
                    diff_positive_vds = positive_minima[1][0] - positive_minima[0][0]
                    print(f"Difference between first two positive minima Vds: {diff_positive_vds}")

                if len(negative_minima) >= 2:
                    diff_negative = negative_minima[1][1] - negative_minima[0][1]
                    print(f"Difference between first two negative minima: {diff_negative}")
                    diff_negative_vds = negative_minima[1][0] - negative_minima[0][0]
                    print(f"Difference between first two negative minima Vds: {diff_negative_vds}")

                if len(positive_minima) > 0 and len(negative_minima) > 0:
                    diff_cross = positive_minima[0][1] - negative_minima[0][1]
                    print(f"Difference between dominant positive and negative minima: {diff_cross}")
                    diff_cross_vds = positive_minima[0][0] - negative_minima[0][0]
                    print(f"Difference between dominant positive and negative minima Vds: {diff_cross_vds}")

                    # Append the calculated values to the table_data list

                sub_folder_path = os.sep.join(label_name.split(os.sep)[:-1]).split('\\')
                table_data.append({
                    'device_name':  sub_folder_path[0],
                    'sub_folder_name':  sub_folder_path[1],
                    'positive_Ids_minima_1': positive_minima[0][1] if len(positive_minima) > 0 else None,
                    'positive_Ids_minima_2': positive_minima[1][1] if len(positive_minima) > 1 else None,
                    'negative_Ids_minima_1': negative_minima[0][1] if len(negative_minima) > 0 else None,
                    'negative_Ids_minima_2': negative_minima[1][1] if len(negative_minima) > 1 else None,
                    'diff_positive_Ids_minima': positive_minima[1][1] - positive_minima[0][1] if len(
                        positive_minima) >= 2 else None,
                    'diff_negative_Ids_minima': negative_minima[1][1] - negative_minima[0][1] if len(
                        negative_minima) >= 2 else None,
                    'positive_Vds_minima_1': positive_minima[0][0] if len(positive_minima) > 0 else None,
                    'positive_Vds_minima_2': positive_minima[1][0] if len(positive_minima) > 1 else None,
                    'negative_Vds_minima_1': negative_minima[0][0] if len(negative_minima) > 0 else None,
                    'negative_Vds_minima_2': negative_minima[1][0] if len(negative_minima) > 1 else None,
                    'diff_positive_Vds_minima': positive_minima[1][0] - positive_minima[0][0] if len(
                        positive_minima) >= 2 else None,
                    'diff_negative_Vds_minima': negative_minima[1][0] - negative_minima[0][0] if len(
                        negative_minima) >= 2 else None,
                    'diff_dominant_positive_negative_Ids_minima': positive_minima[0][1] - negative_minima[0][1] if len(
                        positive_minima) > 0 and len(
                        negative_minima) > 0 else None,
                    'diff_dominant_positive_negative_Vds_minima': positive_minima[0][0] - negative_minima[0][0] if len(
                        positive_minima) > 0 and len(negative_minima) > 0 else None
                })

                # Convert the table_data list to a DataFrame and save it to a CSV file
                table_df = pd.DataFrame(table_data)
                table_df.to_csv('minima_data.csv', index=False)

                print("Minima data saved to minima_data.csv")

                all_positive_minima.extend(positive_minima)
                all_negative_minima.extend(negative_minima)

                plot_data(data, x_column, y_column, log_x, log_y, label=label_name)
                time.sleep(0.2)

            for x, y in all_positive_minima:
                plt.plot(x, y, 'ro')  # Red circle for positive minima
            for x, y in all_negative_minima:
                plt.plot(x, y, 'bo')  # Blue circle for negative minima

            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title(f'Plot of {y_column} vs {x_column}')
            if log_x:
                plt.xlabel(f'Log(|{x_column}|)')
            if log_y:
                plt.ylabel(f'Log(|{y_column}|)')
            plt.grid(True)
            plt.legend()
            plt.show()
            df = pd.DataFrame(table_data)
            numeric_columns = df.select_dtypes(include=['number']).columns
            # Group by 'sub_folder_name' and calculate the mean for each group
            average_df = df.groupby('sub_folder_name')[numeric_columns].mean().reset_index()
            average_df.to_csv('average_minima_data.csv', index=False)

        else:
            for index in selected_files:
                file_path = files[index]
                data = read_csv(file_path)
                plt.figure(figsize=(10, 6))
                label_name = os.path.join(*file_path.split(os.sep)[-3:])
                plot_data(data, x_column, y_column, log_x, log_y, label=label_name)
                positive_minima, negative_minima = find_minima(data, x_column, y_column, log_x, log_y)

                print(f"Minima Calculated from:{label_name}")
                print("Positive Minima:")
                for x, y in positive_minima:
                    print(f"({x}, {y})")

                print("Negative Minima:")
                for x, y in negative_minima:
                    print(f"({x}, {y})")

                if len(positive_minima) >= 2:
                    diff_positive = positive_minima[1][1] - positive_minima[0][1]
                    print(f"Difference between first two positive minima: {diff_positive}")

                if len(negative_minima) >= 2:
                    diff_negative = negative_minima[1][1] - negative_minima[0][1]
                    print(f"Difference between first two negative minima: {diff_negative}")

                if len(positive_minima) > 0 and len(negative_minima) > 0:
                    diff_cross = positive_minima[0][1] - negative_minima[0][1]
                    print(f"Difference between dominant positive and negative minima: {diff_cross}")

                for x, y in positive_minima:
                    plt.plot(x, y, 'ro')  # Red circle for positive minima
                for x, y in negative_minima:
                    plt.plot(x, y, 'bo')  # Blue circle for negative minima

                plt.xlabel(x_column)
                plt.ylabel(y_column)
                plt.title(f'Plot of {y_column} vs {x_column} from {file_path}')
                if log_x:
                    plt.xlabel(f'Log(|{x_column}|)')
                if log_y:
                    plt.ylabel(f'Log(|{y_column}|)')
                plt.grid(True)
                plt.legend()
                plt.show()

        continue_plotting = input("Do you want to continue and replot? (yes/no): ").strip().lower()
        if continue_plotting == 'yes':
            action = input(
                "What would you like to do next? (1. Change directory path, 2. Choose subfolders again, 3. Choose files again): ").strip()
            if action == '1':
                directory_path = None
                subfolders = None
                selected_subfolders = None
                files = None
            elif action == '2':
                subfolders = None
                selected_subfolders = None
                files = None
            elif action == '3':
                files = None
            else:
                print("Invalid action. Please try again.")
        else:
            break
