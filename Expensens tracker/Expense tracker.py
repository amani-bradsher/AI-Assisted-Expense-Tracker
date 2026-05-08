
import json #this is a basic way of storing information in a text file  in like a dictionarie or list way
import os # giving python assess to an operating system module , this allows me to preform task with python it cant do on its own
from datetime import datetime

# File to save data between runs
DATA_FILE = "expenses.json"

# ── Load / Save ──────────────────────────────────────────────
def load_data(): #creates function
    """Load expenses and goal from file, or start fresh."""
    if os.path.exists(DATA_FILE): #checks if the "expenses.json" file already exists
        with open(DATA_FILE, "r") as f: #read mode
            return json.load(f) # reads the JSON file and turns it back into python data
    return {"expenses": [], "goal": None} # if the file don't exist it will default the starting data

def save_data(data):
    """Save expenses and goal to file."""
    with open(DATA_FILE, "w") as f: #write mode
        json.dump(data, f, indent=2) # taking the python data and saves it into a file in JSON format

# ── Menu ─────────────────────────────────────────────────────
def show_menu():
    print("\n==============================")
    print("       EXPENSE TRACKER        ")
    print("==============================")
    print("1. Add expense")
    print("2. View spending")
    print("3. Set goal")
    print("4. View monthly summary")
    print("5. View past months")
    print("6. Reset progress")
    print("7. Exit")
    print("==============================")

# ── Option 1: Add Expense ────────────────────────────────────
CATEGORIES = ["shopping", "food", "transportation", "entertainment", "bills"]
#creating a list for the categories
def add_expense(data):
    """Ask user for category and amount, then save the expense."""
    print("\n-- Add Expense --")
    print("Categories:", ", ".join(CATEGORIES))

    # Get category
    while True:
        category = input("Enter category: ").strip().lower()
        if category in CATEGORIES:
            break
        print(f"Invalid category. Choose from: {', '.join(CATEGORIES)}") # checking to see if you put in an invalid input

    # Get amount
    while True:
        try:
            amount = float(input("Enter amount: $"))
            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.") # checking to see if you put in an invalid input

    # Save expense with today's date
    expense = {
        "category": category,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m")
    }
    data["expenses"].append(expense)
    save_data(data)# saves all the data into the file
    print(f"Saved: ${amount:.2f} for {category}")


# ── Option 2: View Spending ──────────────────────────────────
def view_spending(data):
    print("\n-- View Spending --")

    if not data["expenses"]: # First it checks if there are any expenses , and if not it will stop.
        print("No expenses recorded yet.")
        return

    print(f"\n{'Category':<18} {'Amount':>8}  {'Month'}")  #If there are, it loops through them and prints each one into a table format.
    print("-" * 38)
    for e in data["expenses"]:
        print(f"{e['category']:<18} ${e['amount']:>7.2f}  {e['date']}")

    total = sum(e["amount"] for e in data["expenses"]) #Then here it adds up all the expense amounts, and gets the total and prints it.
    print("-" * 38)
    print(f"{'TOTAL':<18} ${total:>7.2f}")

#In the end if their is a goal set it will compare the total to that goal and tell the user if they are over or under budget.
    if data["goal"]:
        goal = data["goal"]
        print(f"\nYour goal: ${goal:.2f}")
        if total > goal:
            print(f"Over budget by ${total - goal:.2f}!")
        else:
            print(f"Under budget — ${goal - total:.2f} remaining.")
    else:
        print("\nNo goal set. Use option 3 to set one.") # If there’s no goal, it tells them to set one.


# ── Option 3: Set Goal ───────────────────────────────────────
def set_goal(data):
    print("\n-- Set Goal --")
    while True:
        try: #ask the user for an spending goal
            goal = float(input("Enter your spending goal: $"))
            if goal <= 0: # check to see if its over 0
                print("Goal must be greater than zero.")
            else:
                break # will break once a valid number is entered
        except ValueError:
            print("Please enter a valid number.")

    data["goal"] = goal # it saves the goal into the program data and write it in the file.
    save_data(data)
    print(f"Goal set to ${goal:.2f}")


# ── Option 4: Monthly Summary (current month) ────────────────
def monthly_summary(data):
    print("\n-- Monthly Summary --")

    if not data["expenses"]: #First it checks if there are any expenses
        print("No expenses recorded yet.")
        return

    current_month = datetime.now().strftime("%Y-%m") # Its only gets the current month expenses, and filter out the rest
    this_month = [e for e in data["expenses"] if e["date"] == current_month]

    if not this_month: # If there isn't any for that month it will stop
        print(f"No expenses for {current_month} yet.")
        return

    cats = {} # Groups the expenses by category and adds up how much was spent in each one
    for e in this_month:
        cats[e["category"]] = cats.get(e["category"], 0) + e["amount"]

    print(f"\n{current_month}") # Its printing each category with the total spent, and also shows the overall total for the month.
    print("-" * 30)
    month_total = 0
    for cat, total in sorted(cats.items()):
        print(f"  {cat:<18} ${total:.2f}")
        month_total += total
    print(f"  {'Total':<18} ${month_total:.2f}")

    print("\n  Spending by category:") # Creates a simple bar chart using stars to show which category had the most spending
    max_val = max(cats.values())
    for cat, total in sorted(cats.items()):
        bar = "*" * int((total / max_val) * 20)
        print(f"  {cat:<18} {bar} ${total:.2f}")


# ── Option 5: View Past Months ───────────────────────────────
def view_past_months(data):
    print("\n-- Past Months --")

    if not data["expenses"]:
        print("No expenses recorded yet.")
        return

    # Get all the diffrent months and sorting them
    all_months = sorted(set(e["date"] for e in data["expenses"]), reverse=True)
    current_month = datetime.now().strftime("%Y-%m")
    past_months = [m for m in all_months if m != current_month]

    if not past_months:
        print("No past months found. Only the current month has data.")
        return

    # Show list of available months
    print("\nAvailable months:")
    for i, month in enumerate(past_months, 1):
        count = sum(1 for e in data["expenses"] if e["date"] == month)
        total = sum(e["amount"] for e in data["expenses"] if e["date"] == month)
        print(f"  {i}. {month}  ({count} expenses, ${total:.2f} total)")

    print("  0. View all months")

    # Let user pick a month
    while True:
        try:
            choice = int(input("\nSelect a month (0 to view all): "))
            if 0 <= choice <= len(past_months):
                break
            print(f"Enter a number between 0 and {len(past_months)}.")
        except ValueError:
            print("Please enter a valid number.")

    if choice == 0:
        months_to_show = past_months
    else:
        months_to_show = [past_months[choice - 1]]

    # Print summary for selected months
    for month in months_to_show:
        expenses = [e for e in data["expenses"] if e["date"] == month]
        cats = {}
        for e in expenses:
            cats[e["category"]] = cats.get(e["category"], 0) + e["amount"]

        print(f"\n{'=' * 30}")
        print(f"  {month}")
        print(f"{'=' * 30}")
        for cat, total in sorted(cats.items()):
            print(f"  {cat:<18} ${total:.2f}")
        month_total = sum(e["amount"] for e in expenses)
        print(f"  {'-' * 28}")
        print(f"  {'Total':<18} ${month_total:.2f}")

        # show the bar chart of spending that month
        print(f"\n  Spending breakdown:")
        max_val = max(cats.values())
        for cat, total in sorted(cats.items()):
            bar = "*" * int((total / max_val) * 20)
            print(f"  {cat:<18} {bar} ${total:.2f}")


# ── Option 6: Reset Progress ─────────────────────────────────
def reset_progress(data):
    print("\n-- Reset Progress --")
    print("WARNING: This will permanently delete ALL your expenses and goal.")
    print("This cannot be undone!\n")

    confirm = input("Type RESET to confirm, or anything else to cancel: ").strip()

    if confirm == "RESET":
        data["expenses"] = []
        data["goal"] = None
        save_data(data)
        print("All progress has been reset.")
    else:
        print("Reset cancelled. Your data is safe.")


# ── Main Program ─────────────────────────────────────────────
def main():
    print("Opening expense tracker...")
    data = load_data()

    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_expense(data)
        elif choice == "2":
            view_spending(data)
        elif choice == "3":
            set_goal(data)
        elif choice == "4":
            monthly_summary(data)
        elif choice == "5":
            view_past_months(data)
        elif choice == "6":
            reset_progress(data)
        elif choice == "7":
            print("\nGoodbye!")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 7.")

        input("\nPress Enter to return to menu...")


if __name__ == "__main__":
    main()
