import re
from typing import Any

from .values import ALLOWED_CURRENCIES

class Account:
    def __init__(self, iban: str, owner: str, balance: float, overdraft: float = 0.0, currency: str = "UAH") -> None:
        if not self._is_valid_iban(iban):
            raise ValueError(f"Невірний IBAN: {iban}")

        self._iban = iban
        self._currency = currency if currency in ALLOWED_CURRENCIES else "UAH"
        self._overdraft = 0.0
        self._balance = 0.0

        self.owner = owner
        self.overdraft = overdraft
        self.balance = balance

    @property
    def iban(self) -> str:
        return self._iban

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def owner(self) -> str:
        return self._owner

    @owner.setter
    def owner(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Власник рахунку повинен бути непорожнім рядком.")
        self._owner = value.strip()

    @property
    def overdraft(self) -> float:
        return self._overdraft

    @overdraft.setter
    def overdraft(self, value: float) -> None:
        if value < 0:
            raise ValueError("Ліміт кредиту не може бути від'ємним.")
        if self.balance < -value:
            raise ValueError("Ліміт кредиту не може бути меншим за поточний баланс.")
        self._overdraft = float(value)

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        if value < -self.overdraft:
            raise ValueError("Баланс не може бути меншим за ліміт кредиту.")
        self._balance = float(value)


    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Account":
        return cls(
            iban=data.get("iban", ""),
            owner=data.get("owner", ""),
            balance=data.get("balance", 0.0),
            overdraft=data.get("overdraft", 0.0),
            currency=data.get("currency", "UAH")
        )

    @staticmethod
    def _is_valid_iban(iban: str) -> bool:
        # Простий приклад перевірки IBAN (не повна перевірка)
        pattern = r"^[A-Z]{2}\d{2}[A-Z0-9]{1,30}$"
        return bool(re.match(pattern, iban))

    def __repr__(self) -> str:
        return f"Account(iban='{self.iban}', owner='{self.owner}', balance={self.balance}, overdraft={self.overdraft}, currency='{self.currency}')"