"""
E-commerce Sales & Customer Insights Analysis
-----------------------------------------------
Loads raw sales data, cleans it, explores it, and produces the charts
saved in /images for the README and the notebook.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams["figure.dpi"] = 120
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

ACCENT = "#2E5077"
ACCENT2 = "#F2A541"

# ---------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------
df = pd.read_csv("data/ecommerce_sales_data.csv", parse_dates=["order_date"])
print("Raw shape:", df.shape)

# ---------------------------------------------------------------
# 2. Data cleaning
# ---------------------------------------------------------------
before = len(df)
df = df.drop_duplicates(subset=["order_id"])
print(f"Removed {before - len(df)} duplicate orders")

# fix bad quantity entries (negative values are data-entry errors, not returns)
bad_qty = (df["quantity"] <= 0).sum()
df = df[df["quantity"] > 0]
print(f"Removed {bad_qty} rows with invalid quantity")

# fill missing payment method with 'Unknown' rather than dropping the order
df["payment_method"] = df["payment_method"].fillna("Unknown")

# recompute revenue after cleaning
df["revenue"] = df["quantity"] * df["unit_price"]

df["month"] = df["order_date"].dt.to_period("M").astype(str)

print("Clean shape:", df.shape)
print("Missing values after cleaning:\n", df.isna().sum())

# ---------------------------------------------------------------
# 3. KPIs
# ---------------------------------------------------------------
total_revenue = df["revenue"].sum()
total_orders = df["order_id"].nunique()
avg_order_value = df.groupby("order_id")["revenue"].sum().mean()
unique_customers = df["customer_id"].nunique()

print("\n--- KPIs ---")
print(f"Total revenue: Rs {total_revenue:,.0f}")
print(f"Total orders: {total_orders}")
print(f"Average order value: Rs {avg_order_value:,.0f}")
print(f"Unique customers: {unique_customers}")

# ---------------------------------------------------------------
# 4. Monthly revenue trend
# ---------------------------------------------------------------
monthly = df.groupby("month")["revenue"].sum().sort_index()

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(monthly.index, monthly.values, marker="o", color=ACCENT, linewidth=2)
ax.fill_between(monthly.index, monthly.values, color=ACCENT, alpha=0.08)
ax.set_title("Monthly Revenue Trend", fontsize=13, fontweight="bold")
ax.set_ylabel("Revenue (Rs)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("images/01_monthly_revenue_trend.png")
plt.close()

# ---------------------------------------------------------------
# 5. Revenue by category
# ---------------------------------------------------------------
cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.barh(cat_rev.index, cat_rev.values, color=ACCENT)
ax.set_title("Revenue by Category", fontsize=13, fontweight="bold")
ax.set_xlabel("Revenue (Rs)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))
for bar in bars:
    w = bar.get_width()
    ax.text(w, bar.get_y() + bar.get_height()/2, f" {w/1000:.0f}k", va="center", fontsize=9)
plt.tight_layout()
plt.savefig("images/02_revenue_by_category.png")
plt.close()

# ---------------------------------------------------------------
# 6. Revenue by region
# ---------------------------------------------------------------
region_rev = df.groupby("region")["revenue"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(6.5, 4.5))
colors = [ACCENT, ACCENT2, "#8FA6C9", "#C9C9C9"]
ax.pie(region_rev.values, labels=region_rev.index, autopct="%1.0f%%",
       colors=colors, startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
ax.set_title("Revenue Share by Region", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("images/03_revenue_by_region.png")
plt.close()

# ---------------------------------------------------------------
# 7. Top 10 products by revenue
# ---------------------------------------------------------------
top_products = df.groupby("product")["revenue"].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(top_products.index[::-1], top_products.values[::-1], color=ACCENT2)
ax.set_title("Top 10 Products by Revenue", fontsize=13, fontweight="bold")
ax.set_xlabel("Revenue (Rs)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))
plt.tight_layout()
plt.savefig("images/04_top_products.png")
plt.close()

# ---------------------------------------------------------------
# 8. Customer segmentation: new vs repeat customers
# ---------------------------------------------------------------
order_counts = df.groupby("customer_id")["order_id"].nunique()
repeat_customers = (order_counts > 1).sum()
new_customers = (order_counts == 1).sum()

fig, ax = plt.subplots(figsize=(5.5, 4.5))
ax.pie([new_customers, repeat_customers], labels=["One-time", "Repeat"],
       autopct="%1.0f%%", colors=[ACCENT, ACCENT2], startangle=90,
       wedgeprops={"edgecolor": "white", "linewidth": 1.5})
ax.set_title("Customer Type: One-time vs Repeat", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("images/05_customer_segments.png")
plt.close()

# ---------------------------------------------------------------
# 9. Payment method distribution
# ---------------------------------------------------------------
pay_counts = df["payment_method"].value_counts()

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(pay_counts.index, pay_counts.values, color=ACCENT)
ax.set_title("Orders by Payment Method", fontsize=13, fontweight="bold")
ax.set_ylabel("Number of Orders")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("images/06_payment_methods.png")
plt.close()

print("\nAll charts saved to /images")

# ---------------------------------------------------------------
# 10. Save a small summary for the README
# ---------------------------------------------------------------
top_category = cat_rev.idxmax()
top_region = region_rev.idxmax()
top_product = top_products.idxmax()
repeat_pct = repeat_customers / (repeat_customers + new_customers) * 100

with open("insights_summary.txt", "w") as f:
    f.write(f"Total revenue: Rs {total_revenue:,.0f}\n")
    f.write(f"Total orders: {total_orders}\n")
    f.write(f"Unique customers: {unique_customers}\n")
    f.write(f"Average order value: Rs {avg_order_value:,.0f}\n")
    f.write(f"Top category: {top_category} (Rs {cat_rev.max():,.0f})\n")
    f.write(f"Top region: {top_region} ({region_rev.max()/total_revenue*100:.0f}% of revenue)\n")
    f.write(f"Best-selling product: {top_product}\n")
    f.write(f"Repeat customer rate: {repeat_pct:.0f}%\n")

print("\nSummary written to insights_summary.txt")
