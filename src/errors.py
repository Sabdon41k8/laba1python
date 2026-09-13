class BankError(Exception):
    """Базовий клас для всіх винятків, які виникають у API Bank."""
    pass

class EntityNotFound(BankError):
    """Виникає, коли запитувана сутність не знайдена."""
    def __init__(self, iban: str):
        super().__init__(f"Сутність з IBAN '{iban}' не знайдена.")
        self.iban = iban