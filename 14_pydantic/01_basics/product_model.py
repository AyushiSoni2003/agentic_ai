from pydantic import BaseModel

class Product(BaseModel):
    id : int
    name : str
    price : float
    in_stock : bool = True

product_one = Product(id = 101, name = "Laptop", price = 999.99 , in_stock = True)

product_two = Product(id =2 , name = "Mouse", price = 25.50)

print(product_one)
print(product_two)