from typing import Iterator, Union, Any
from entities import Account
from errors import EntityNotFound
from decorators import validated


# ЗАВДАННЯ 3.2 клас для ітерації по сторінках
class LedgerPageIterator:
    def __init__(self, ledger: "Ledger", page_size: int) -> None:
        self._ledger = ledger
        self._page_size = page_size
        self._current_index = 0

    def __iter__(self) -> Iterator[list[Account]]:
        return self

    def __next__(self) -> list[Account]:
        if self._current_index >= len(self._ledger):
            raise StopIteration

        page = [
            self._ledger[i]
            for i in range(self._current_index, min(self._current_index + self._page_size, len(self._ledger)))
        ]
        self._current_index += self._page_size
        return page


class Ledger:
    def __init__(self, accounts: list[Account] | None = None) -> None:
        self._accounts: list[Account] = []
        self._index: dict[str, Account] = {}

        if accounts:
            for acc in accounts:
                self.add_account(acc)

    def add_account(self, account: Account) -> None:
        if account.iban in self._index:
            return
        self._accounts.append(account)
        self._index[account.iban] = account

    # ЗАВДАННЯ 3.1. Інтерфейс колекції
    def __len__(self) -> int:
        return len(self._accounts)

    def __getitem__(self, index: int | slice) -> Union[Account, "Ledger"]:
        if isinstance(index, slice):
            # Повертає новий екземпляр колекції того самого типу!
            return Ledger(self._accounts[index])
        return self._accounts[index]

    def __contains__(self, item: object) -> bool:
        if isinstance(item, str):
            return item in self._index
        if isinstance(item, Account):
            return item.iban in self._index
        return False

    def __iter__(self) -> Iterator[Account]:
        return iter(self._accounts)

    # ЗАВДАННЯ 3.2. Посторінковий обхід
    def pages(self, page_size: int) -> LedgerPageIterator:
        return LedgerPageIterator(self, page_size)

    # ЗАВДАННЯ 3.3. Виклик екземпляра як запит
    def __call__(self, **kwargs: Any) -> "Ledger":
        allowed = {"currency", "min_balance"}
        for key in kwargs:
            if key not in allowed:
                raise TypeError(f"Невідомий критерій '{key}'. Дозволені: {allowed}")

        result = self._accounts
        if "currency" in kwargs:
            result = [a for a in result if a.currency == kwargs["currency"]]
        if "min_balance" in kwargs:
            result = [a for a in result if a.balance >= kwargs["min_balance"]]

        return Ledger(result)

    # ЗАВДАННЯ 3.4. Пошук сутності за IBAN
    def get(self, iban: str) -> Account:
        try:
            return self._index[iban]
        except KeyError:
            raise EntityNotFound(iban) from None

    # ЗАВДАННЯ 4. Підтримка арифметичних операцій
    def __add__(self, other: object) -> "Ledger":
        if not isinstance(other, Ledger):
            return NotImplemented
        new_ledger = Ledger(self._accounts.copy())
        for acc in other:
            new_ledger.add_account(acc)
        return new_ledger

    def __radd__(self, other: object) -> "Ledger":
        if other == 0:
            return Ledger(self._accounts.copy())
        return NotImplemented

    # ЗАВДАННЯ 5.
    @validated(amount="positive", currency="one_of:UAH,USD,EUR")
    def deposit(self, iban: str, amount: float, currency: str) -> None:
        acc = self.get(iban)
        if acc.currency != currency:
            raise ValueError("Валюта поповнення не збігається з валютою рахунку.")
        acc.balance += amount