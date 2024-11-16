from datetime import date
import json
from tkinter import Tk
from Part_C_W20929095 import FinanceTrackerGUI

# List to store all transactions
transactions = {}

def load_transactions():
    """
    Load transactions from the 'transactions.json' file.
    Returns:
        dict: A dictionary containing the loaded transactions, or an empty dictionary if the file doesn't exist or is corrupted.
    """
    global transactions
    try:
        with open("transactions.json", "r") as file:
            transactions = json.load(file)
            return transactions
    except FileNotFoundError:
        print("The file does not exist")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
        return {}

def load_transactions_from_file(file_path):
    """
    Read transactions from a text file and add them to the transactions dictionary.
    Args:
        file_path (str): The path of the file to load transactions from.
    """
    global transactions
    try:
        with open(file_path, "r") as file:
            for line in file:
                transaction_data = line.strip().split(",")
                transaction_type = transaction_data[0].lower()
                amount = float(transaction_data[1])
                date_str = transaction_data[2]

                data = {"amount": amount, "date": date_str}

                if transaction_type not in transactions:
                    transactions[transaction_type] = []
                transactions[transaction_type].append(data)

        print(f"Transactions loaded successfully from {file_path}")
        while True:
            save = input("Do you want to save ? Y/N :").lower()
            if save == 'y':
                save_transactions(transactions)
                return
            if save =='n':
                return
            else:
                print("Please Enter Y/N.")
                
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")            

def save_transactions(data):
    """
    Save the transactions data to the 'transactions.json' file.
    Args:
        data (dict): A dictionary containing all transactions to be saved to the file.
    """
    try:
        with open("transactions.json", "w") as file:
            json.dump(data, file)
            print("Data Saved Succesfully!")
    except json.JSONDecodeError as e:
        print(f"Error: {e}")

def add_transaction(selected_type=None, index=None):
    """
    Add a new transaction or update an existing transaction.
    Args:
        selected_type (str, optional): The type of transaction to be updated. If None, a new transaction is added.
        index (int, optional): The index of the transaction to be updated. If None, a new transaction is added.
    """
    global transactions

    # Prompt the user to enter transaction details
    transaction_type = input("Enter transaction type: ").lower()
    while True:
        try:
            amount = float(input("Enter the amount: "))
            break
        except ValueError:
            print("Invalid input! , Please enter a number.")
    today_date = str(date.today())
    data = {"amount": amount, "date": today_date}

    # Add or update the transaction based on the provided index
    if index is None:
        if transaction_type not in transactions:
            transactions[transaction_type] = []
        transactions[transaction_type].append(data)
        print("Your transaction added successfully")
    else:
        if selected_type not in transactions:
            print(f"Invalid transaction type: {selected_type}")
            main_menu()
            return

        if transaction_type not in transactions.keys():
            if len(transactions[selected_type]) == 1:
                del transactions[selected_type]
            else:
                del transactions[selected_type][index - 1]
            transactions[transaction_type] = []
            transactions[transaction_type] = [data]
            print("Your transaction updated successfully")
        else:
            if len(transactions[selected_type]) == 1:
                del transactions[selected_type]
                transactions[transaction_type].append(data)
            else:
                del transactions[selected_type][index - 1]
                transactions[transaction_type]= [data]
            print("Your transaction updated successfully")

    # Save the updated transactions list to the file
    save_transactions(transactions)
    main_menu()

def view_transactions():
    """
    Display all transactions in the transactions dictionary.
    """
    if len(transactions) == 0:
        print("\nNo transaction recorded")
    else:
        print("\nALL Transactions")
        for transaction_type, transaction_list in transactions.items():
            for i, transaction in enumerate(transaction_list, start=1):
                print(f"""
                        Transaction Number: {i}
                        Transaction Type: {transaction_type}
                        Amount: {transaction['amount']}
                        Transaction Date: {transaction['date']}
""")
                
def update_transaction():
    """
    Allow the user to update an existing transaction in the transactions dictionary.
    """
    global transactions
    if len(transactions) == 0:
        print("\nNo transactions yet to be updated!")
        main_menu()
    else:
        review_transactions = input("Do you want to see the transactions before update ( Enter-Y/N ) : ").lower()
        if review_transactions == 'y':
            view_transactions()

        for name in transactions.keys():
            print(f"- {name}")

        selected_type = input(f"Enter the transaction type to update: ").lower()
        if selected_type in transactions:
            data = transactions[selected_type]
            print(f"Transactions for '{selected_type}':")
            for index, transaction in enumerate(data):
                print(f"Index-{index}. Amount: {transaction['amount']}, Date: {transaction['date']}")
        index = int(input(f"Enter the index of the transaction to update for '{selected_type}': "))
        if 0 <= index < len(data):
            question = input("Do you want to update this ( enter-Y/N ): ").lower()
            if question == 'y':
                add_transaction(selected_type, index)
            else:
                print("Invalid input. Returning to main menu.")
                main_menu()
        else:
            print("Invalid transaction. Returning to main menu.")
            main_menu()

def delete_transaction():
    """
    Allow the user to delete an existing transaction from the transactions dictionary.
    """
    global transactions
    if len(transactions) == 0:
        print("\nNo transactions records found")
        main_menu()
    else:
        review_transactions = input("Do you want to see the transactions before delete ( Enter-Y/N ) : ").lower()
        if review_transactions == 'y':
            view_transactions()
        for name in transactions.keys():
            print(f"- {name}")
        try:
            selected_type = input(f"Enter the transaction type to delete: ").lower()
            if selected_type in transactions.keys():
                data = transactions[selected_type]
                print(f"Transactions for '{selected_type}':")
                for index, transaction in enumerate(data):
                    print(f"\nindex-{index} Amount: {transaction['amount']}, Date: {transaction['date']}")
                index = int(input(f"Enter the index of the transaction to delete for '{selected_type}': "))
                if 0 <= index <= len(selected_type):
                    question = input("Do you want to delete this ( enter-Y/N ): ").lower()
                    if question == "y":
                        if len(transactions[selected_type]) == 1:
                             del transactions[selected_type]
                             print("Your transaction deleted successfully")
                             save_transactions(transactions)
  
                        else:
                            del transactions[selected_type][index]
                            print("Your transaction deleted successfully")
                            save_transactions(transactions)
                    else:
                        print("Transaction not deleted. Returning to main menu.")
                        main_menu()
                else:
                    print("Invalid transaction index. Returning to main menu.")
        except ValueError:
            print("Invalid input. Returning to main menu.")
def display_summary():
        """
        Display a summary of the transactions in the transactions dictionary.
        """
        transaction_count, incomes_count, expenses_count, total_incomes, total_expenses = 0, 0, 0, 0, 0
        if not transactions:
            print("\nNo transactions records found")
            main_menu()
        else:
            print("\nSummary of the transactions")
            amount = 0
            for transaction_type, data in transactions.items():
                for transaction in data:
                    transaction_count += 1
                    amount += transaction['amount']
            print(f"Total Transactions: {transaction_count}")
            print(f"Tota Amount       : {amount}")

            main_menu()

def main_menu():
    """
    Display the main menu and handle user choices.
    """
    load_transactions()
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Load Transactions from File")
        print("7. Launch GUI")  # New menu option
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary()
        elif choice == '6':
            file_path = input("Enter the file path: ")
            load_transactions_from_file(file_path)
        elif choice == '7':  # Launch the GUI
            root = Tk()
            app = FinanceTrackerGUI(root)
            root.mainloop()
        elif choice == '8':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()