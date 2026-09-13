import copy
from typing import Optional, Type
from types import TracebackType
from collections_ import Ledger


class BankSession:
    def __init__(self, ledger: Ledger) -> None:
        self.ledger = ledger
        self._snapshot: Optional[Ledger] = None

    def __enter__(self) -> Ledger:
        # Зберігаємо знімок стану на випадок помилки
        self._snapshot = copy.deepcopy(self.ledger)
        return self.ledger

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> bool:
        if exc_type is not None:
            # Скасовуємо всі зміни
            self.ledger._accounts = self._snapshot._accounts
            self.ledger._index = self._snapshot._index
        # Повертаємо False -> виняток НЕ приховується
        return False