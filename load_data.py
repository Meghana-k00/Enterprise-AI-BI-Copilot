import pandas as pd
import pyodbc

# Load CSV files
customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")
sales = pd.read_csv("data/sales.csv")

# SQL Server connection
connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    r"SERVER=.\MSSQLSERVER01;"
    "DATABASE=EnterpriseBI;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

# Allow faster batch inserts
cursor.fast_executemany = True

# Clear existing data so the script can safely be rerun
cursor.execute("DELETE FROM dbo.Sales")
cursor.execute("DELETE FROM dbo.Products")
cursor.execute("DELETE FROM dbo.Customers")

# Insert customers
customer_data = [
    tuple(row)
    for row in customers[
        ["customer_id", "customer_name", "segment", "country", "region"]
    ].itertuples(index=False, name=None)
]

cursor.executemany(
    """
    INSERT INTO dbo.Customers
    (customer_id, customer_name, segment, country, region)
    VALUES (?, ?, ?, ?, ?)
    """,
    customer_data
)

# Insert products
product_data = [
    tuple(row)
    for row in products[
        ["product_id", "product_name", "category", "subcategory", "cost"]
    ].itertuples(index=False, name=None)
]

cursor.executemany(
    """
    INSERT INTO dbo.Products
    (product_id, product_name, category, subcategory, cost)
    VALUES (?, ?, ?, ?, ?)
    """,
    product_data
)

# Insert sales
sales_data = [
    tuple(row)
    for row in sales[
        [
            "order_id",
            "order_date",
            "customer_id",
            "product_id",
            "quantity",
            "unit_price",
            "discount",
            "sales_amount",
            "region",
        ]
    ].itertuples(index=False, name=None)
]

cursor.executemany(
    """
    INSERT INTO dbo.Sales
    (
        order_id,
        order_date,
        customer_id,
        product_id,
        quantity,
        unit_price,
        discount,
        sales_amount,
        region
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    sales_data
)

connection.commit()

print("Data loaded successfully.")
print(f"Customers loaded: {len(customer_data)}")
print(f"Products loaded: {len(product_data)}")
print(f"Sales loaded: {len(sales_data)}")

cursor.close()
connection.close()