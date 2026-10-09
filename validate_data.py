import pandas as pd

sales = pd.read_csv("data/sales.csv")
customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")

print("SALES")
print(sales)
print("\nSales rows:", len(sales))

print("\nCUSTOMERS")
print(customers)
print("\nCustomer rows:", len(customers))

print("\nPRODUCTS")
print(products)
print("\nProduct rows:", len(products))