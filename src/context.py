import copy
from typing import Optional, Type
from types import TracebackType

from .collections import Ledger


class BankSession:
    def __init__(self, ledger: Ledger) -> None:
        self.ledger = ledger
        self._snapshot: Optional[Ledger] = None
        self._original_accounts = []
        self._original_index = {}

    def __enter__(self) -> Ledger:
        # Зберігаємо знімок стану на випадок помилки
        self._snapshot = copy.deepcopy(self.ledger)
        self._original_accounts = list(self.ledger._accounts)
        self._original_index = dict(self.ledger._index)
        return self.ledger

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> bool:
        if exc_type is not None:
            # Скасовуємо всі зміни
            snapshot_by_iban = {account.iban: account for account in self._snapshot._accounts}
            for account in self._original_accounts:
                account.__dict__.update(snapshot_by_iban[account.iban].__dict__)
            self.ledger._accounts = self._original_accounts
            self.ledger._index = self._original_index
        # Повертаємо False -> виняток НЕ приховується
        return False