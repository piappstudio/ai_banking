from faker import Faker
from curd.curd_helper import create_customer, create_account, create_transaction, transfer_funds
import random

fake = Faker()

def seed_random_data():
    """
    Populate the database with random test data:
    - 25 customers
    - Each with 1 to 3 accounts
    - 500 total transactions (including inter-account transfers)
    """
    customer_ids = []
    account_ids = []

    # Step 1: Create 25 random customers
    for _ in range(25):
        name = fake.name()
        email = fake.unique.email()
        phone = fake.msisdn()[:10]
        cust_id = create_customer(name, email, phone)
        customer_ids.append(cust_id)

    # Step 2: Create accounts for each customer
    for cust_id in customer_ids:
        for _ in range(random.randint(1, 3)):  # Each customer has 1–3 accounts
            account_number = str(random.randint(1000000000, 9999999999))
            balance = round(random.uniform(1000, 100000), 2)
            acc_id = create_account(cust_id, account_number, balance)
            account_ids.append(acc_id)

    # Step 3: Create 500 total transactions
    for i in range(500):
        if random.random() < 0.2:  # 20% fund transfers
            from_acc, to_acc = random.sample(account_ids, 2)
            amount = round(random.uniform(10, 2000), 2)
            transfer_funds(from_acc, to_acc, amount, description="Random Fund Transfer")
        else:
            acc_id = random.choice(account_ids)
            transaction_type = random.choice(["credit", "debit"])
            amount = round(random.uniform(10, 5000), 2)
            description = fake.sentence(nb_words=4)
            create_transaction(acc_id, transaction_type, amount, description)

    print("✅ Database seeded with random data successfully!")


# Run the seeding
if __name__ == "__main__":
    seed_random_data()
