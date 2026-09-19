import numpy as np
import pandas as pd

np.random.seed(42)

n = 1200

categories = {
    "Electronics": ["Wireless Earbuds", "Smartphone Case", "Bluetooth Speaker", "Power Bank", "Smartwatch"],
    "Fashion": ["Cotton T-Shirt", "Denim Jeans", "Running Shoes", "Backpack", "Sunglasses"],
    "Home & Kitchen": ["Non-stick Pan", "LED Desk Lamp", "Water Bottle", "Storage Box", "Coffee Mug"],
    "Beauty": ["Face Wash", "Moisturizer", "Lipstick", "Hair Serum", "Sunscreen"],
    "Sports": ["Yoga Mat", "Resistance Bands", "Skipping Rope", "Cricket Bat", "Football"],
}
regions = ["North", "South", "East", "West"]
payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Net Banking"]

rows = []
start_date = pd.Timestamp("2025-01-01")
for i in range(n):
    category = np.random.choice(list(categories.keys()), p=[0.28, 0.24, 0.18, 0.16, 0.14])
    product = np.random.choice(categories[category])
    order_date = start_date + pd.Timedelta(days=int(np.random.randint(0, 365)))
    quantity = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.35, 0.2, 0.15, 0.15, 0.1, 0.05])
    base_price = {
        "Electronics": np.random.uniform(499, 2999),
        "Fashion": np.random.uniform(299, 1799),
        "Home & Kitchen": np.random.uniform(199, 1499),
        "Beauty": np.random.uniform(149, 899),
        "Sports": np.random.uniform(249, 1999),
    }[category]
    unit_price = round(base_price, 2)
    customer_id = f"CUST{np.random.randint(1, 480):04d}"
    region = np.random.choice(regions, p=[0.3, 0.27, 0.22, 0.21])
    payment = np.random.choice(payment_methods, p=[0.38, 0.22, 0.18, 0.14, 0.08])
    rating = np.random.choice([1,2,3,4,5, np.nan], p=[0.02,0.03,0.1,0.35,0.4,0.1])

    rows.append([
        f"ORD{10000+i}", order_date, customer_id, category, product,
        quantity, unit_price, region, payment, rating
    ])

df = pd.DataFrame(rows, columns=[
    "order_id", "order_date", "customer_id", "category", "product",
    "quantity", "unit_price", "region", "payment_method", "rating"
])

# introduce a few realistic messy rows so cleaning has something real to do
dupe_rows = df.sample(15, random_state=1)
df = pd.concat([df, dupe_rows], ignore_index=True)

null_idx = df.sample(20, random_state=2).index
df.loc[null_idx, "payment_method"] = np.nan

neg_idx = df.sample(5, random_state=3).index
df.loc[neg_idx, "quantity"] = -1  # bad data entry to be cleaned

df["revenue"] = df["quantity"] * df["unit_price"]

df.to_csv("data/ecommerce_sales_data.csv", index=False)
print(df.shape)
print(df.head())
