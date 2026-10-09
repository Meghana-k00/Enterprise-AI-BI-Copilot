from .sql_connection import get_connection


def get_database_schema():
    connection = get_connection()
    cursor = connection.cursor()

    schema = """
DATABASE: EnterpriseBI

TABLE: Customers
- customer_id VARCHAR(20) PRIMARY KEY
- customer_name VARCHAR(100)
- segment VARCHAR(50)
- country VARCHAR(50)
- region VARCHAR(50)

TABLE: Products
- product_id VARCHAR(20) PRIMARY KEY
- product_name VARCHAR(100)
- category VARCHAR(50)
- subcategory VARCHAR(50)
- cost DECIMAL(10,2)

TABLE: Sales
- order_id INT PRIMARY KEY
- order_date DATE
- customer_id VARCHAR(20)
- product_id VARCHAR(20)
- quantity INT
- unit_price DECIMAL(10,2)
- discount DECIMAL(5,2)
- sales_amount DECIMAL(12,2)
- region VARCHAR(50)

RELATIONSHIPS:
- Sales.customer_id → Customers.customer_id
- Sales.product_id → Products.product_id

IMPORTANT:
- sales_amount represents the final sales amount after discount.
- Revenue should be calculated using sales_amount.
"""

    cursor.close()
    connection.close()

    return schema