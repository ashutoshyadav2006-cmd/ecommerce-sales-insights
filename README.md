# E-commerce Sales & Customer Insights Dashboard

A data cleaning + exploratory analysis project on e-commerce order data, built as the
capstone for the **Data Analytics with Python & Power BI** internship (EduSkills Academy).
This repo contains the Python/Pandas side of the analysis; the same cleaned dataset was
also used to build an interactive Power BI dashboard.

## What this project does

- Cleans a raw orders dataset (duplicate orders, invalid quantities, missing payment methods)
- Explores revenue trends over time, by category, region, and product
- Segments customers into one-time vs repeat buyers
- Summarizes payment method usage
- Produces the charts used in the final dashboard

## Key insights

- **Total revenue:** ₹18,24,508 across 1,195 clean orders
- **Average order value:** ₹1,527
- **Top category:** Electronics (₹8,01,710)
- **Top region:** South (31% of revenue)
- **Best-selling product:** Bluetooth Speaker
- **Repeat customer rate:** 78% — most customers came back for more than one order

## Charts

**Monthly revenue trend**

![Monthly revenue trend](01_monthly_revenue_trend.png)

**Revenue by category**

![Revenue by category](02_revenue_by_category.png)

**Revenue share by region**

![Revenue by region](03_revenue_by_region.png)

**Top 10 products by revenue**

![Top products](04_top_products.png)

**Customer type: one-time vs repeat**

![Customer segments](05_customer_segments.png)

**Orders by payment method**

![Payment methods](06_payment_methods.png)

## Tech stack

- Python (Pandas, NumPy) — data cleaning & aggregation
- Matplotlib — visualization
- Jupyter Notebook — analysis walkthrough (see `ecommerce_sales_analysis.ipynb`)

## Project structure

```
├── ecommerce_sales_data.csv          # raw order-level dataset
├── ecommerce_sales_analysis.ipynb    # full analysis with outputs
├── analysis.py                       # script version of the analysis
├── generate_data.py                  # generates the sample dataset
├── 01_monthly_revenue_trend.png      # exported charts
├── 02_revenue_by_category.png
├── 03_revenue_by_region.png
├── 04_top_products.png
├── 05_customer_segments.png
├── 06_payment_methods.png
└── README.md
```

## Running it yourself

```bash
pip install pandas numpy matplotlib
python analysis.py
```

This regenerates all charts and prints the key metrics to the console.

---
*Part of the Data Analytics with Python & Power BI internship, EduSkills Academy.*
