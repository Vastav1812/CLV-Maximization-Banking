# file: generate_data.py

import random
import string
import csv
import datetime
import faker

fake = faker.Faker()

NUM_CUSTOMERS = 10000
NUM_TRANSACTIONS = 100000
NUM_CALLS = 20000

# 1. Generate Customer Master Data
def generate_customers(num_customers=10000):
    customers = []
    for _ in range(num_customers):
        customer_id = fake.unique.random_int(min=100000, max=999999)
        age = random.randint(18, 80)
        region = random.choice(["North", "South", "East", "West"])
        join_date = fake.date_between(start_date='-5y', end_date='today')
        # You can add more attributes like income, occupation, etc.
        
        customers.append({
            "customer_id": customer_id,
            "age": age,
            "region": region,
            "join_date": join_date.strftime("%Y-%m-%d")
        })
    return customers

# 2. Generate Transaction Data
def generate_transactions(customers, num_transactions=100000):
    transactions = []
    product_categories = ["Loans", "Credit Card", "Savings", "Mortgage", "Insurance"]
    
    for _ in range(num_transactions):
        cust = random.choice(customers)
        transaction_date = fake.date_between(start_date='-2y', end_date='today')
        amount = round(random.uniform(10, 5000), 2)  # Range of $10 to $5000
        product = random.choice(product_categories)
        
        transactions.append({
            "customer_id": cust["customer_id"],
            "transaction_date": transaction_date.strftime("%Y-%m-%d"),
            "transaction_amount": amount,
            "product_category": product
        })
    return transactions

# 3. Generate Support Call Logs
def generate_support_calls(customers, num_calls=20000):
    calls = []
    # Simple categories of issues and random text
    issue_categories = ["Account Issue", "Payment Problem", "General Inquiry", "Complaint"]
    churn_keyword_samples = [
        "cancel my account", 
        "very unhappy", 
        "thinking of leaving", 
        "poor service"
    ]
    
    for _ in range(num_calls):
        cust = random.choice(customers)
        call_date = fake.date_between(start_date='-1y', end_date='today')
        issue = random.choice(issue_categories)
        
        # Generate a simple transcript with a random chance of including a churn phrase
        transcript = fake.sentence(nb_words=10)
        if random.random() < 0.3:  # ~30% calls mention churn-related frustration
            transcript += " " + random.choice(churn_keyword_samples)
        
        calls.append({
            "call_id": fake.unique.random_int(min=1000000, max=9999999),
            "customer_id": cust["customer_id"],
            "call_date": call_date.strftime("%Y-%m-%d"),
            "issue_category": issue,
            "call_transcript": transcript
        })
    return calls

# 4. Write Data to CSV
def write_to_csv(data, filename, fieldnames):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    print("Generating synthetic data...")
    customers_list = generate_customers(NUM_CUSTOMERS)
    transactions_list = generate_transactions(customers_list, NUM_TRANSACTIONS)
    calls_list = generate_support_calls(customers_list, NUM_CALLS)
    
    write_to_csv(customers_list, "data/raw/customers.csv", ["customer_id", "age", "region", "join_date"])
    write_to_csv(transactions_list, "data/raw/transactions.csv", ["customer_id", "transaction_date", "transaction_amount", "product_category"])
    write_to_csv(calls_list, "data/raw/support_calls.csv", ["call_id", "customer_id", "call_date", "issue_category", "call_transcript"])
    
    print("Data generation complete!")
