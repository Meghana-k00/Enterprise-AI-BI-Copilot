import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    r"SERVER=.\MSSQLSERVER01;"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

connection = pyodbc.connect(connection_string)
connection.autocommit = True

cursor = connection.cursor()

cursor.execute("""
IF DB_ID('EnterpriseBI') IS NULL
BEGIN
    CREATE DATABASE EnterpriseBI
END
""")

print("EnterpriseBI database is ready.")

cursor.close()
connection.close()