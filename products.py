class Product:
    def __init__(self, name: str, price: float, quantity: int):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty")
        if not isinstance(price, (int, float)) or isinstance(price, bool):
            raise TypeError(f"Expected price to be a number, got {type(price).__name__}")
        if price < 0:
            raise ValueError(f"Price cannot be negative, got {price}")

        self.name = name
        self.price = price
        self.active = True
        self.set_quantity(quantity)

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError(
                f"Expected quantity to be an int, got {type(quantity).__name__}"
            )
        if quantity < 0:
            raise ValueError(f"Quantity cannot be negative, got {quantity}")

        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def show(self):
        print(f"{self.name}, Price: {self.price}, Quantity: {self.quantity}")

    def buy(self, quantity: int) -> float:
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError(
                f"Expected quantity to be an int, got {type(quantity).__name__}"
            )
        if quantity < 1:
            raise ValueError("Quantity cannot be smaller than 1")
        if quantity > self.quantity:
            raise ValueError(
                f"Cannot buy {quantity} units; only {self.quantity} in stock"
            )

        self.set_quantity(self.quantity - quantity)
        return float(self.price * quantity)

# if __name__ == "__main__":
#     bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
#     mac = Product("MacBook Air M2", price=1450, quantity=101)

#     print(bose.buy(50))
#     print(mac.buy(100))
#     print(mac.is_active())

#     bose.show()
#     mac.show()

#     bose.set_quantity(1000)
#     bose.show()