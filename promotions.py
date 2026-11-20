from abc import ABC, abstractmethod


class Promotion(ABC):
    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Promotion name cannot be empty")
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        pass

class PercentDiscount(Promotion):
    def __init__(self, name: str, percent: float):
        super().__init__(name)
        if not isinstance(percent, (int, float)) or isinstance(percent, bool):
            raise TypeError(f"Expected percent to be a number, got {type(percent).__name__}")
        if not (0 <= percent <= 100):
            raise ValueError(f"Percent must be between 0 and 100, got {percent}")
        
        self.percent = percent

    def apply_promotion(self, product, quantity: int) -> float:
        return float(product.price * quantity * (1 - self.percent / 100))

class SecondHalfPrice(Promotion):
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity: int) -> float:
        half_items = quantity // 2
        full_items = quantity - half_items
        return float((product.price * full_items) + (half_items * product.price * 0.5))

class ThirdOneFree(Promotion):
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity: int) -> float:
        free_items = quantity // 3
        paid_items = quantity - free_items
        return float(paid_items * product.price)