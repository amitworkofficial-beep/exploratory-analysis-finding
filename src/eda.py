import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# LOAD DATASET
# ============================================================

file_path = "data/raw/Online Retail.xlsx"
df = pd.read_excel(file_path)

# Calculate transaction revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]


# ============================================================
# DATASET OVERVIEW
# ============================================================

print("========== DATASET OVERVIEW ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


print("\n========== COLUMN INFORMATION ==========")
df.info()


print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())


print("\n========== DUPLICATE ROWS ==========")
print("Duplicate rows:", df.duplicated().sum())


print("\n========== NUMERICAL SUMMARY ==========")
print(df[["Quantity", "UnitPrice", "CustomerID"]].describe())


print("\n========== UNIQUE VALUES ==========")
print("Unique invoices:", df["InvoiceNo"].nunique())
print("Unique products:", df["StockCode"].nunique())
print("Unique customers:", df["CustomerID"].nunique())
print("Unique countries:", df["Country"].nunique())


print("\n========== COUNTRY DISTRIBUTION ==========")
print(df["Country"].value_counts().head(10))


print("\n========== NEGATIVE QUANTITIES ==========")
print("Negative quantity rows:", (df["Quantity"] < 0).sum())


print("\n========== ZERO/NEGATIVE PRICES ==========")
print("Zero price rows:", (df["UnitPrice"] == 0).sum())
print("Negative price rows:", (df["UnitPrice"] < 0).sum())


# ============================================================
# REVENUE ANALYSIS
# ============================================================

print("\n========== REVENUE SUMMARY ==========")
print(df["Revenue"].describe())


print("\n========== TOTAL REVENUE ==========")
print("Total revenue:", df["Revenue"].sum())


print("\n========== POSITIVE VS NEGATIVE REVENUE ==========")
print("Positive revenue rows:", (df["Revenue"] > 0).sum())
print("Negative revenue rows:", (df["Revenue"] < 0).sum())
print("Zero revenue rows:", (df["Revenue"] == 0).sum())


# ============================================================
# MONTHLY REVENUE
# ============================================================

print("\n========== MONTHLY REVENUE ==========")

df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

monthly_revenue = (
    df.groupby("YearMonth")["Revenue"]
    .sum()
    .reset_index()
)

print(monthly_revenue.to_string(index=False))


print("\n========== HIGHEST REVENUE MONTHS ==========")

top_months = (
    monthly_revenue
    .sort_values("Revenue", ascending=False)
    .head(10)
)

print(top_months.to_string(index=False))


print("\n========== LOWEST REVENUE MONTHS ==========")

bottom_months = (
    monthly_revenue
    .sort_values("Revenue", ascending=True)
    .head(10)
)

print(bottom_months.to_string(index=False))


# ============================================================
# TOP PRODUCTS
# ============================================================

print("\n========== TOP PRODUCTS BY REVENUE ==========")

product_revenue = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(product_revenue)


# ============================================================
# TOP COUNTRIES
# ============================================================

print("\n========== TOP COUNTRIES BY REVENUE ==========")

country_revenue = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(country_revenue)


# ============================================================
# NOVEMBER 2011 ANALYSIS
# ============================================================

november_period = pd.Period("2011-11", freq="M")

november_df = df[
    df["YearMonth"] == november_period
]


print("\n========== TOP PRODUCTS IN NOVEMBER 2011 ==========")

november_products = (
    november_df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(november_products)


print("\n========== TOP COUNTRIES IN NOVEMBER 2011 ==========")

november_countries = (
    november_df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(november_countries)


# ============================================================
# MONTHLY SALES VOLUME
# ============================================================

print("\n========== MONTHLY SALES VOLUME ==========")

monthly_sales = (
    df.groupby("YearMonth")
    .agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum"),
        Invoices=("InvoiceNo", "nunique"),
        Customers=("CustomerID", "nunique")
    )
    .reset_index()
)

print(monthly_sales.to_string(index=False))


# ============================================================
# NOVEMBER SUMMARY
# ============================================================

print("\n========== NOVEMBER 2011 SUMMARY ==========")

november_summary = monthly_sales[
    monthly_sales["YearMonth"] == november_period
]

print(november_summary.to_string(index=False))


# ============================================================
# AVERAGE MONTHLY REVENUE
# ============================================================

print("\n========== AVERAGE MONTHLY REVENUE (FULL MONTHS) ==========")

# December 2011 is incomplete, so exclude it.
full_months = monthly_sales[
    monthly_sales["YearMonth"] != pd.Period("2011-12", freq="M")
]

average_revenue = full_months["Revenue"].mean()

print("Average monthly revenue:", average_revenue)

november_revenue = november_summary["Revenue"].iloc[0]

print("November revenue:", november_revenue)

print(
    "November vs average:",
    ((november_revenue / average_revenue) - 1) * 100,
    "%"
)


# ============================================================
# REVENUE PER CUSTOMER
# ============================================================

print("\n========== REVENUE PER CUSTOMER ==========")

monthly_customer_value = monthly_sales.copy()

monthly_customer_value["RevenuePerCustomer"] = (
    monthly_customer_value["Revenue"]
    / monthly_customer_value["Customers"]
)

print(
    monthly_customer_value[
        ["YearMonth", "Revenue", "Customers", "RevenuePerCustomer"]
    ].to_string(index=False)
)


print("\n========== NOVEMBER REVENUE PER CUSTOMER ==========")

november_rpc = monthly_customer_value[
    monthly_customer_value["YearMonth"] == november_period
]["RevenuePerCustomer"].iloc[0]

print("November revenue per customer:", november_rpc)


# ============================================================
# SEPTEMBER TO NOVEMBER GROWTH
# ============================================================

print("\n========== SEPTEMBER TO NOVEMBER GROWTH ==========")

comparison_months = [
    pd.Period("2011-09", freq="M"),
    pd.Period("2011-10", freq="M"),
    pd.Period("2011-11", freq="M")
]

comparison = monthly_sales[
    monthly_sales["YearMonth"].isin(comparison_months)
].copy()

print(comparison.to_string(index=False))


september_revenue = comparison[
    comparison["YearMonth"] == pd.Period("2011-09", freq="M")
]["Revenue"].iloc[0]

november_revenue = comparison[
    comparison["YearMonth"] == pd.Period("2011-11", freq="M")
]["Revenue"].iloc[0]


september_customers = comparison[
    comparison["YearMonth"] == pd.Period("2011-09", freq="M")
]["Customers"].iloc[0]

november_customers = comparison[
    comparison["YearMonth"] == pd.Period("2011-11", freq="M")
]["Customers"].iloc[0]


september_invoices = comparison[
    comparison["YearMonth"] == pd.Period("2011-09", freq="M")
]["Invoices"].iloc[0]

november_invoices = comparison[
    comparison["YearMonth"] == pd.Period("2011-11", freq="M")
]["Invoices"].iloc[0]


print(
    "Revenue growth Sep to Nov:",
    ((november_revenue / september_revenue) - 1) * 100,
    "%"
)

print(
    "Customer growth Sep to Nov:",
    ((november_customers / september_customers) - 1) * 100,
    "%"
)

print(
    "Invoice growth Sep to Nov:",
    ((november_invoices / september_invoices) - 1) * 100,
    "%"
)


# ============================================================
# CHART 1 - MONTHLY REVENUE
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["YearMonth"].astype(str),
    monthly_sales["Revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/monthly_revenue_trend.png")
plt.show()


# ============================================================
# CHART 2 - MONTHLY CUSTOMERS
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["YearMonth"].astype(str),
    monthly_sales["Customers"],
    marker="o"
)

plt.title("Monthly Customer Count")
plt.xlabel("Month")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/monthly_customer_count.png")
plt.show()


# ============================================================
# CHART 3 - MONTHLY INVOICES
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["YearMonth"].astype(str),
    monthly_sales["Invoices"],
    marker="o"
)

plt.title("Monthly Number of Invoices")
plt.xlabel("Month")
plt.ylabel("Number of Invoices")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/monthly_invoice_count.png")
plt.show()


# ============================================================
# CHART 4 - TOP 10 PRODUCTS
# ============================================================

top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(12, 6))

plt.barh(
    top_products.index,
    top_products.values
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig("outputs/top_10_products_revenue.png")
plt.show()


# ============================================================
# CHART 5 - TOP 10 COUNTRIES
# ============================================================

top_countries = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(12, 6))

plt.barh(
    top_countries.index,
    top_countries.values
)

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig("outputs/top_10_countries_revenue.png")
plt.show()


print("\n========== ANALYSIS COMPLETED SUCCESSFULLY ==========")