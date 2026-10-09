import pyodbc


CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    r"SERVER=.\MSSQLSERVER01;"
    "DATABASE=EnterpriseBI;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)


def get_connection():
    return pyodbc.connect(CONNECTION_STRING)