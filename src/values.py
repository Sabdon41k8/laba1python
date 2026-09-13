import functools
from dataclasses import dataclass

ALLOWED_CURRENCIES = ["USD", "EUR", "UAH"]

@functools.total_ordering
class Money:
    # __slots__ обмежує атрибути класу Money
    __slots__ = ("currency", "amount", "_frozen")

    def __init__(self, currency: str, amount: float) -> None:
        if currency not in ALLOWED_CURRENCIES:
            raise ValueError(f"Валюта '{currency}' не підтримується. Допустимі валюти: {ALLOWED_CURRENCIES}")

        #обходимо обмеження __slots__ і встановлюємо атрибути безпосередньо через object.__setattr__
        object.__setattr__(self, "currency", currency)
        object.__setattr__(self, "amount", round(float(amount), 2))
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: object) -> None:
        # Забороняємо змінювати атрибути після ініціалізації
        if getattr(self, "_frozen", False):
            raise AttributeError(f"Об'єкт {self.__class__.__name__} є незмінним (frozen).")
        object.__setattr__(self, name, value)

    # ЗАВДАННЯ 1.3 вивідення інформації про об'єкт
    def __repr__(self) -> str:
        return f"Money(currency='{self.currency}', amount={self.amount})"  

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"

    # ЗАВДАННЯ 1.4 порівняння об'єктів
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return (self.currency, self.amount) == (other.currency, other.amount)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError(f"Неможливо порівнювати об'єкти з різними валютами: {self.currency} та {other.currency}")
        return self.amount < other.amount

    # ЗАВДАННЯ 1.5 хешування об'єктів
    def __hash__(self) -> int:
        return hash((self.currency, self.amount))

    # ЗАВДАННЯ 4 підтримка арифметичних операцій
    def __add__(self, other: object) -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError(f"Різні валюти: {self.currency} та {other.currency}")
        return Money(self.currency, self.amount + other.amount)

    def __sub__(self, other: object) -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError(f"Різні валюти: {self.currency} та {other.currency}")
        return Money(self.currency, self.amount - other.amount)

    def __mul__(self, other: float) -> "Money":
        if not isinstance(other, (int, float)):
            return NotImplemented
        return Money(self.currency, self.amount * other)

    def __rmul__(self, other: float) -> "Money":
        return self.__mul__(other)


# ЗАВДАННЯ 1.2 альтернатива через dataclass
@dataclass(frozen=True, slots=True)
class MoneyDataClass:
    currency: str
    amount: float

