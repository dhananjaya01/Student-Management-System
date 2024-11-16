import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime

class FinanceTrackerGUI:
    def __init__(self, root):
        """
        Initializes the FinanceTrackerGUI class.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.create_widgets()
        self.transactions = self.load_transactions("transactions.json")
        self.display_transactions(self.transactions)

    def create_widgets(self):
        """
        Creates the widgets for the GUI, including the table, scrollbar, and search bar.
        """
        # Frame for table and scrollbar
        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=10)

        # Treeview for displaying transactions
        self.table = ttk.Treeview(table_frame, columns=("Date", "Category", "Amount"))
        self.table.heading("#0", text="")
        self.table.column("#0", width=25, anchor="center")

        self.table.heading("Date", text="Date", command=lambda: self.sort_by_column("Date", False))
        self.table.column("Date", width=100, anchor="w")

        self.table.heading("Category", text="Category", command=lambda: self.sort_by_column("Category", False))
        self.table.column("Category", width=200, anchor="w")

        self.table.heading("Amount", text="Amount", command=lambda: self.sort_by_column("Amount", False))
        self.table.column("Amount", width=100, anchor="e")

        self.table.pack(side=tk.LEFT)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.BOTH)
        self.table.configure(yscrollcommand=scrollbar.set)

        # Search bar and button
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10)

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(search_frame, text="Search", command=self.search_transactions)
        search_button.pack(side=tk.LEFT)

    def load_transactions(self, filename):
        """
        Loads transactions from a JSON file.

        Args:
            filename (str): The name of the JSON file to load transactions from.

        Returns:
            list: A list of dictionaries representing the loaded transactions.
        """
        try:
            with open("transactions.json", "r") as file:
                data = json.load(file)
                self.transactions = []
                for category, transaction_list in data.items():
                    for transaction in transaction_list:
                        self.transactions.append({
                            "category": category,
                            "date": transaction["date"],
                            "amount": transaction["amount"]
                        })
                return self.transactions
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading transactions: {e}")
            return []

    def display_transactions(self, transactions):
        """
        Displays the transactions in the Treeview table.

        Args:
            transactions (list): A list of dictionaries representing the transactions to be displayed.
        """
        self.table.delete(*self.table.get_children())

        for transaction in transactions:
            amount = transaction["amount"]
            color = "green" if amount >= 0 else "red"
            self.table.insert("", "end", values=(transaction["date"], transaction["category"], amount), tags=(color,))

        self.table.tag_configure("green", foreground="green")
        self.table.tag_configure("red", foreground="red")

    def search_transactions(self):
        """
        Searches for transactions based on the user's input in the search bar.
        """
        query = self.search_entry.get().lower()
        results = []
        for transaction in self.transactions:
            if query in str(transaction["date"]).lower() or \
               query in transaction["category"].lower() or \
               query in str(transaction["amount"]):
                results.append(transaction)
        self.display_transactions(results)

    def sort_by_column(self, column, reverse):
        """
        Sorts the transactions based on the selected column and order.

        Args:
            column (str): The column to sort by ("Date", "Category", or "Amount").
            reverse (bool): Whether to sort in reverse order.
        """
        self.transactions.sort(key=lambda x: x["date" if column == "Date" else "category" if column == "Category" else "amount"], reverse=reverse)
        self.display_transactions(self.transactions)

        # Toggle the sorting order
        self.table.heading(column, text=column, command=lambda col=column: self.sort_by_column(col, not reverse))

def main():
    """
    Runs the main function to create the GUI application.
    """
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()