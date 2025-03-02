#!/usr/bin/env python
# coding: utf-8

# In[4]:


import csv
from collections import defaultdict

# Initialize dictionaries to track expenses and reimbursements
expenses = defaultdict(float)
specific_owed = defaultdict(lambda: defaultdict(float))
amount_due = defaultdict(float)
individual_due = defaultdict(lambda: defaultdict(float))

# Read the list of people from the People CSV file
def read_people(file_path):
    with open(file_path, mode='r') as people_file:
        reader = csv.reader(people_file)
        return {row[0].strip() for row in reader if row}

all_people = read_people('Trip Expense Calculator - People.csv')

# Process expenses from multiple CSV files
def process_expenses(file_path):
    with open(file_path, mode='r') as expenses_file:
        reader = csv.reader(expenses_file)
        next(reader)  # Skip the header row

        for row in reader:
            if not row or not row[0]:  # Skip empty rows
                continue

            expense = row[0]
            cost = float(row[1])
            purchaser = row[2].strip()
            will_reimburse = [p.strip() for p in row[3].split(',')] if row[3] else []
            
            # Track expenses
            expenses[purchaser] += cost
            
            # Determine who is splitting the cost
            if will_reimburse and will_reimburse[0].lower() == "all":
                split_among = all_people
            else:
                split_among = set(will_reimburse) | {purchaser}  # Include purchaser

            split_cost = cost / len(split_among)
            
            for person in split_among:
                if person != purchaser:  # Exclude self-payment
                    specific_owed[person][purchaser] += split_cost
                    amount_due[purchaser] += split_cost
                    individual_due[purchaser][person] += split_cost

# Process expense files
expense_files = ['Trip Expense Calculator - Expenses.csv'] 
for file in expense_files:
    process_expenses(file)

# Output the reimbursement details
for reimburser, debtors in specific_owed.items():
    if debtors:
        print(f"{reimburser} should pay:")
        for debtor, amount in debtors.items():
            if amount > 0:
                print(f"- {debtor}: ${amount:.2f}")

# Output the total amount each purchaser should receive with individual amounts
print("\nTotal amount each purchaser should receive:")
for purchaser, amount in amount_due.items():
    breakdown = ", ".join([f"{person}: ${amt:.2f}" for person, amt in individual_due[purchaser].items()])
    print(f"{purchaser}: ${amount:.2f} ({breakdown})")

