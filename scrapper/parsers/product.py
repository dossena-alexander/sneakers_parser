# class Cost():
#     value: int
#     currency: str

#     def __init__(self, value: int, currency: str) -> None:
#         self.value = value
#         self.currency = currency

#     def __str__(self) -> str:
#         return f'{self.value} {self.currency}'

#     def __dict__(self) -> dict:
#         return {
#             'value': self.value,
#             'currency': self.currency
#         }
    
#     def dict(self) -> dict:
#         return self.__dict__()


# class Product():
#     name: str
#     details: dict


#     def __init__(self,
#                  name: str,
#                  details: dict) -> None:
#         self.name = name
#         self.details = details

#     def __dict__(self):
#         dict()


# class Sneakers(Product):
#     sizes: dict

class Product(dict): ...