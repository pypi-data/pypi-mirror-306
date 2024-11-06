from _plot_from_subfolders_until_user_terminate import _plot_from_subfolders_until_user_terminate
from _plot_only_user_requested_column import _plot_only_user_requested_column
import threading

def run_function(choice):
    if choice == '1':
        threading.Thread(target=_plot_from_subfolders_until_user_terminate).start()
    elif choice == '2':
        threading.Thread(target=_plot_only_user_requested_column).start()
    else:
        print("Invalid choice. Please select 1 or 2, or enter 'q' to quit.")
        return True
    return False

def main():
    while True:
        user_input = input("Enter 1 to plot from subfolders or 2 to plot single file or q to quit: ")
        if user_input.lower() == 'q':
            print("Terminating the program.")
            break
        if run_function(user_input):
            continue
        break

if __name__ == "__main__":
    main()
