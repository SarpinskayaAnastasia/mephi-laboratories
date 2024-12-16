from random import randint


class SavingAccount:
    def __init__(self, percent: float, default_income=0):
        self.balance = default_income
        self.percent = percent  # используется только для вывода
        self.rate = 1.0 + percent / 100

    def add_money(self, summ):
        self.balance += summ * self.rate
        print(f"Saving account was topped up by {summ}. Percents accrued: {summ * self.rate - summ}")
        return None

    def transfer(self, summ):
        if summ <= self.balance:
            self.balance -= summ
            print(f"Saving account balance decreased by {summ}")
            return True
        print('Not enough money')
        return False

    def __str__(self):
        return f"Saving account with a rate of {self.percent}"


class InvestmentAccount:
    def __init__(self, default_income: float):
        self.balance = default_income
        self.is_blocked = False

    def block(self):
        if self.balance < 0:
            self.is_blocked = True
            print("Investment account has blocked")
            return None
        print("Investment account cannot be blocked")
        return None

    def change(self):
        self.balance += randint(-500, 500 + 1)
        self.block()
        return None

    def add_money(self, summ):
        self.change()
        if summ < 0:
            return None
        self.balance += summ
        print(f'Investment account balance increased by {summ}')
        if self.balance > 0 and self.is_blocked:
            self.is_blocked = False
            print("Investment account doesn't blocked anymore.")
            return None
        return None

    def transfer(self, summ):
        self.change()
        if self.is_blocked:
            return False
        if summ <= self.balance:
            self.balance -= summ
            print(f'Investment account balance decreased by {summ}')
            return True
        print('Not enough money')
        return False

    def __str__(self):
        return ('BLOCKED ' * int(self.is_blocked)) + f'Investment account in the amount of {self.balance}' + (
                ' BLOCKED' * int(self.is_blocked))


if __name__ == "__main__":
    sa_example = SavingAccount("small", 999)
    print(sa_example)
    sa_example.add_money(88888888)
    print(sa_example.balance)
    sa_example.transfer(99)
    sa_example.transfer(234567898765432)
    ia_example = InvestmentAccount(888888.00)
    print(ia_example)
    ia_example.block()
    print(ia_example)
    ia_example.add_money(777)
    print(ia_example)
    ia_example.change()
    print(ia_example)
    ia_example.transfer(888888.00 + 777)  # let's try to withdraw that count of money which we added on IA
    ia_example.transfer(12345678908765432)
    print(ia_example)
