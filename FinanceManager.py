import csv
import os
from datetime import datetime

class PersonalFinanceManager:
    def __init__(self, data_file='finance_data.csv'):
        self.data_file = data_file
        self.fields = ['Date', 'Category', 'Description', 'Amount', 'Type']  # Type: Income/Expense
        if not os.path.exists(self.data_file):
            self.create_file()

    def create_file(self):
        with open(self.data_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.fields)

    def add_transaction(self, category, description, amount, transaction_type):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.data_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, description, amount, transaction_type])
        print("Transaction added successfully.")

    def view_transactions(self, transaction_type=None):
        with open(self.data_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if transaction_type is None or row['Type'].lower() == transaction_type.lower():
                    print(row)

    def calculate_balance(self):
        balance = 0.0
        with open(self.data_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                amount = float(row['Amount'])
                if row['Type'].lower() == 'income':
                    balance += amount
                elif row['Type'].lower() == 'expense':
                    balance -= amount
        return balance

    def generate_report(self):
        total_income = 0.0
        total_expense = 0.0
        category_expense = {}
        with open(self.data_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                amount = float(row['Amount'])
                if row['Type'].lower() == 'income':
                    total_income += amount
                elif row['Type'].lower() == 'expense':
                    total_expense += amount
                    category_expense[row['Category']] = category_expense.get(row['Category'], 0) + amount
        
        print("Total Income: $", total_income)
        print("Total Expense: $", total_expense)
        print("Net Balance: $", total_income - total_expense)
        print("\nExpenses by Category:")
        for category, amount in category_expense.items():
            print(f"{category}: ${amount}")

    def set_budget(self, category, limit):
        with open('budget.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([category, limit])
        print(f"Budget set for {category} at ${limit}")

    def check_budget(self):
        budgets = {}
        with open('budget.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    budgets[row[0]] = float(row[1])
        
        category_spent = {}
        with open(self.data_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Type'].lower() == 'expense':
                    category_spent[row['Category']] = category_spent.get(row['Category'], 0) + float(row['Amount'])
        
        print("\nBudget Status:")
        for category, limit in budgets.items():
            spent = category_spent.get(category, 0)
            print(f"{category}: Spent ${spent} / Budget ${limit} - {'Over Budget!' if spent > limit else 'Within Budget'}")

    def calculate_investment_growth(self, initial_amount, years, annual_return_rate):
        future_value = initial_amount * ((1 + (annual_return_rate / 100)) ** years)
        print(f"Investment Growth: After {years} years, ${initial_amount} will grow to ${future_value:.2f}")
        return future_value

if __name__ == "__main__":
    manager = PersonalFinanceManager()
    while True:
        print("\n--- Personal Finance Manager ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Calculate Balance")
        print("5. Generate Report")
        print("6. Set Budget")
        print("7. Check Budget")
        print("8. Investment Growth Calculator")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            category = input("Enter category: ")
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            manager.add_transaction(category, description, amount, 'Income')
        elif choice == '2':
            category = input("Enter category: ")
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            manager.add_transaction(category, description, amount, 'Expense')
        elif choice == '3':
            manager.view_transactions()
        elif choice == '4':
            print("Current Balance: $", manager.calculate_balance())
        elif choice == '5':
            manager.generate_report()
        elif choice == '6':
            category = input("Enter category: ")
            limit = float(input("Enter budget limit: "))
            manager.set_budget(category, limit)
        elif choice == '7':
            manager.check_budget()
        elif choice == '8':
            initial = float(input("Enter initial investment: "))
            years = int(input("Enter number of years: "))
            rate = float(input("Enter annual return rate (in %): "))
            manager.calculate_investment_growth(initial, years, rate)
        elif choice == '9':
            print("Exiting... Have a great day!")
            break
        else:
            print("Invalid choice, please try again.")
