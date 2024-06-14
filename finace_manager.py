import json
from datetime import datetime

class Entry:
    def __init__(self, amount, category, date, description, entry_type):
        self.amount = amount
        self.category = category
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.description = description
        self.entry_type = entry_type  # 'income' or 'expense'

    def __str__(self):
        return f"{self.date.date()} - {self.category} - {self.entry_type.capitalize()}: ${self.amount:.2f} ({self.description})"

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date.strftime("%Y-%m-%d"),
            "description": self.description,
            "entry_type": self.entry_type
        }

def add_entry(entries, amount, category, date, description, entry_type):
    entry = Entry(amount, category, date, description, entry_type)
    entries.append(entry)

def view_entries(entries, filter_type=None, filter_value=None):
    for i, entry in enumerate(entries, 1):
        if filter_type == "date" and entry.date.date() != filter_value:
            continue
        if filter_type == "category" and entry.category != filter_value:
            continue
        print(f"{i}. {entry}")

def update_entry(entries, index, amount=None, category=None, date=None, description=None):
    if 0 <= index < len(entries):
        if amount:
            entries[index].amount = amount
        if category:
            entries[index].category = category
        if date:
            entries[index].date = datetime.strptime(date, "%Y-%m-%d")
        if description:
            entries[index].description = description

def delete_entry(entries, index):
    if 0 <= index < len(entries):
        entries.pop(index)

def save_entries(entries, filename="entries.json"):
    with open(filename, "w") as file:
        json.dump([entry.to_dict() for entry in entries], file)

def load_entries(filename="entries.json"):
    try:
        with open(filename, "r") as file:
            entries_data = json.load(file)
            return [Entry(**data) for data in entries_data]
    except FileNotFoundError:
        return []

def generate_report(entries):
    total_income = sum(entry.amount for entry in entries if entry.entry_type == "income")
    total_expenses = sum(entry.amount for entry in entries if entry.entry_type == "expense")
    balance = total_income - total_expenses

    category_expenses = {}
    for entry in entries:
        if entry.entry_type == "expense":
            if entry.category not in category_expenses:
                category_expenses[entry.category] = 0
            category_expenses[entry.category] += entry.amount

    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Balance: ${balance:.2f}")
    print("Expenses by Category:")
    for category, amount in category_expenses.items():
        print(f"  {category}: ${amount:.2f}")

def main():
    entries = load_entries()
    while True:
        print("\nPersonal Finance Manager")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Entries")
        print("4. Update Entry")
        print("5. Delete Entry")
        print("6. Generate Report")
        print("7. Save and Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            date = input("Enter date (YYYY-MM-DD): ")
            description = input("Enter description: ")
            add_entry(entries, amount, category, date, description, "income")
        elif choice == '2':
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            date = input("Enter date (YYYY-MM-DD): ")
            description = input("Enter description: ")
            add_entry(entries, amount, category, date, description, "expense")
        elif choice == '3':
            filter_type = input("Filter by date (d) or category (c)? (leave blank for no filter): ")
            filter_value = None
            if filter_type == 'd':
                filter_value = datetime.strptime(input("Enter date (YYYY-MM-DD): "), "%Y-%m-%d").date()
                view_entries(entries, "date", filter_value)
            elif filter_type == 'c':
                filter_value = input("Enter category: ")
                view_entries(entries, "category", filter_value)
            else:
                view_entries(entries)
        elif choice == '4':
            index = int(input("Enter entry number to update: ")) - 1
            amount = input("Enter new amount (leave blank to keep unchanged): ")
            category = input("Enter new category (leave blank to keep unchanged): ")
            date = input("Enter new date (YYYY-MM-DD, leave blank to keep unchanged): ")
            description = input("Enter new description (leave blank to keep unchanged): ")
            update_entry(entries, index, float(amount) if amount else None, category, date, description)
        elif choice == '5':
            index = int(input("Enter entry number to delete: ")) - 1
            delete_entry(entries, index)
        elif choice == '6':
            generate_report(entries)
        elif choice == '7':
            save_entries(entries)
            print("Entries saved. Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
