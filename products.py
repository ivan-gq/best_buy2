from promotions import Promotion
from functools import total_ordering

@total_ordering
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
        self.promotion: Promotion | None = None
        self.quantity = quantity

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price == other.price

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price > other.price

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        if price < 0:
            raise ValueError("Negative age not allowed")
        else:
            self._price = price

    @property
    def quantity(self) -> int:
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity: int) -> None:
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError(
                f"Expected quantity to be an int, got {type(quantity).__name__}"
            )
        if quantity < 0:
            raise ValueError(f"Quantity cannot be negative, got {quantity}")

        self._quantity = quantity
        if self._quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def __str__(self):
        promo_text = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, {promo_text}"

    def show(self):
        print(self)

    def get_promotion(self) -> Promotion | None:
        return self.promotion

    def set_promotion(self, promotion: Promotion | None) -> None:
        if promotion is not None and not isinstance(promotion, Promotion):
            raise TypeError(
                f"Expected a Promotion instance or None, got {type(promotion).__name__}"
            )
        self.promotion = promotion

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

        self.quantity = self.quantity - quantity
        if self.promotion is not None:
            return float(self.promotion.apply_promotion(self, quantity))
        return float(self.price * quantity)



class NonStockedProduct(Product):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, 0)
        self.activate()

    @Product.quantity.setter
    def quantity(self, quantity: int) -> None:
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError(
                f"Expected quantity to be an int, got {type(quantity).__name__}"
            )
        if quantity < 0:
            raise ValueError(f"Quantity cannot be negative, got {quantity}")

        self._quantity = 0
        self.activate()

    def buy(self, quantity: int) -> float:
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError(
                f"Expected quantity to be an int, got {type(quantity).__name__}"
            )
        if quantity < 1:
            raise ValueError("Quantity cannot be smaller than 1")
        if self.promotion is not None:
            return float(self.promotion.apply_promotion(self, quantity))
        return float(self.price * quantity)

    def __str__(self):
        promo_text = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: Unlimited, {promo_text}"



class LimitedProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        if not isinstance(maximum, int) or isinstance(maximum, bool):
            raise TypeError(
                f"Expected maximum to be an int, got {type(maximum).__name__}"
            )
        if maximum < 1:
            raise ValueError(f"Maximum per order must be at least 1, got {maximum}")

        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError(
                f"Expected quantity to be an int, got {type(quantity).__name__}"
            )
        if quantity > self.maximum:
            raise ValueError(
                f"Cannot buy {quantity} of {self.name}; maximum per order is {self.maximum}"
            )

        return super().buy(quantity)

    def __str__(self):
        promo_text = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Maximum: {self.maximum}, {promo_text}"

#if __name__ == "__main__":

#     bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
#     mac = Product("MacBook Air M2", price=1450, quantity=101)

#     print(bose.buy(50))
#     print(mac.buy(100))
#     print(mac.is_active())

#     bose.show()
#     mac.show()

#     bose.set_quantity(1000)
#     bose.show()