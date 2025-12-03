import csv
from datetime import datetime

CSV_FILE = "data.csv"

def load_data():
    try:
        with open(CSV_FILE, "r") as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        return []

def add_expense():
    date = datetime.now().strftime("%Y-%m-%d")
    item = input("Enter item: ")
    amount = input("Enter amount: ")
    category = input("Enter category: ")

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, item, amount, category])

    print("Expense added successfully!")

def view_expenses():
    rows = load_data()
    print("\n---- All Expenses ----")
    for row in rows:
        print(row)

def total_expense():
    rows = load_data()
    total = sum(float(r[2]) for r in rows)
    print(f"\nTotal Expenses: ${total}")

def main():
    while True:
        print("\n1. Add Expense")
        print("2. View All")
        print("3. Total Spending")
        print("4. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            total_expense()
        elif choice == "4":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
