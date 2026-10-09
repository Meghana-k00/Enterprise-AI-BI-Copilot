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

cursor.execute("""
IF OBJECT_ID('dbo.Customers', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Customers (
        customer_id VARCHAR(20) PRIMARY KEY,
        customer_name VARCHAR(100),
        segment VARCHAR(50),
        country VARCHAR(50),
        region VARCHAR(50)
    )
END
""")

cursor.execute("""
IF OBJECT_ID('dbo.Products', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Products (
        product_id VARCHAR(20) PRIMARY KEY,
        product_name VARCHAR(100),
        category VARCHAR(50),
        subcategory VARCHAR(50),
        cost DECIMAL(10,2)
    )
END
""")

cursor.execute("""
IF OBJECT_ID('dbo.Sales', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Sales (
        order_id INT PRIMARY KEY,
        order_date DATE,
        customer_id VARCHAR(20),
        product_id VARCHAR(20),
        quantity INT,
        unit_price DECIMAL(10,2),
        discount DECIMAL(5,2),
        sales_amount DECIMAL(12,2),
        region VARCHAR(50),
        FOREIGN KEY (customer_id) REFERENCES dbo.Customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES dbo.Products(product_id)
    )
END
""")

connection.commit()

print("Business tables created successfully.")

cursor.close()
connection.close()