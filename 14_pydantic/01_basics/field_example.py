from pydantic import BaseModel
from typing import List, Dict , Optional

class Cart(BaseModel):
    id : int
    items : List[str]
    quantities : Dict[str,int]

class BlogPost(BaseModel):
    title : str
    content : str
    image_url : Optional[str]


cart_data = { 
    "id" : 123,
    "items" : ["Laptop" , "Mouse"],
    "quantities" : {"Laptop" : 1 , "Mouse" : 2}
}

cart = Cart(**cart_data)

print(cart)
