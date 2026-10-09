import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    r"SERVER=.\MSSQLSERVER01;"
    "DATABASE=EnterpriseBI;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

queries = {
    "Customers": "SELECT COUNT(*) FROM dbo.Customers",
    "Products": "SELECT COUNT(*) FROM dbo.Products",
    "Sales": "SELECT COUNT(*) FROM dbo.Sales",
}

for table, query in queries.items():
    cursor.execute(query)
    count = cursor.fetchone()[0]
    print(f"{table}: {count} rows")

print("\nSample Sales:")
cursor.execute("""
SELECT TOP 5
    order_id,
    order_date,
    customer_id,
    product_id,
    sales_amount
FROM dbo.Sales
ORDER BY order_date
""")

for row in cursor.fetchall():
    print(row)

cursor.close()
connection.close()