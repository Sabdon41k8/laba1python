from src import Money, Account, Ledger, BankSession, EntityNotFound


def main() -> None:
    print("--- 1. Демонстрація Money (Value Object) ---")
    m1 = Money("UAH", 100)
    m2 = Money("UAH", 100)
    print(f"m1 is m2: {m1 is m2} | m1 == m2: {m1 == m2}")  # False, True
    print(f"У set: {len({m1, m2})}")  # 1 (завдяки __hash__ і __eq__)

    try:
        m1.amount = 200
    except AttributeError as e:
        print(f"Успішно перехоплено спробу зміни: {e}")

    print("\n--- 2. Демонстрація Account (Entity & Property) ---")
    acc1 = Account("UA11111111111111111111111111", "Іван Петренко", 1000, overdraft=200)
    acc2 = Account("UA22222222222222222222222222", "Олена Коваль", 500)
    acc3 = Account("UA33333333333333333333333333", "Олег Сидор", 1500, currency="USD")

    try:
        acc1.balance = -500  # Перевищує overdraft=200
    except ValueError as e:
        print(f"Перехоплено порушення овердрафту: {e}")

    acc_from_dict = Account.from_dict({"iban": "UA44444444444444444444444444", "owner": "Ганна", "balance": 100})
    print(f"Створено з dict: {acc_from_dict}")

    print("\n--- 3. Демонстрація Ledger (Collection) ---")
    ledger = Ledger([acc1, acc2, acc3, acc_from_dict])
    print(f"Розмір: {len(ledger)}")
    print(f"Тип зрізу [0:2]: {type(ledger[0:2])}")

    print("Посторінковий обхід (розмір 2):")
    for page in ledger.pages(2):
        print("  Сторінка:", page)

    print("Фільтрація ledger(currency='UAH', min_balance=600):")
    filtered = ledger(currency="UAH", min_balance=600)
    for a in filtered:
        print(" ", a)

    try:
        ledger.get("UA00000000000000000000000000")
    except EntityNotFound as e:
        print(f"EAFP перехоплення: {e}")

    print("\n--- 4. Перевантаження операторів ---")
    print(f"Money + Money: {Money('UAH', 50) + Money('UAH', 30)}")
    print(f"Money * 3: {Money('USD', 20) * 3}")

    l1 = Ledger([acc1])
    l2 = Ledger([acc2])
    l3 = Ledger([acc3])
    print(f"sum([l1, l2, l3]): {len(sum([l1, l2, l3]))} елементів")

    try:
        l1 + 10
    except TypeError:
        print("Перехоплено TypeError при додаванні числового значення")

    print("\n--- 5. Валідаційний декоратор ---")
    print(f"Назва методу після @wraps: '{Ledger.deposit.__name__}'")
    try:
        ledger.deposit(acc1.iban, -50, "UAH")
    except ValueError as e:
        print(f"Декоратор відхилив від'ємний депозит: {e}")

    print("\n--- 6. Контекстний менеджер BankSession ---")
    print(f"Баланс acc1 до транзакції: {acc1.balance}")
    try:
        with BankSession(ledger):
            acc1.balance += 500
            print(f"Тимчасовий баланс усередині with: {acc1.balance}")
            raise RuntimeError("Помилка під час обробки транзакції!")
    except RuntimeError:
        print("Перехоплено помилку виконання сесії.")

    print(f"Баланс acc1 після відкату: {acc1.balance}")


if __name__ == "__main__":
    main()