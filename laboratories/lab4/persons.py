from income_accounts import SavingAccount, InvestmentAccount
from cards import Card, search_card
from random import choice


class Person:
    def __init__(self, first_name: str, last_name: str, cards: list) -> None:
        self.fn = first_name
        self.ln = last_name
        self.cards = cards
        self.sa = []

    def __str__(self) -> str:
        return f"{self.fn} {self.ln}"

    def buy(self, product: str, cost: float):
        if not self.cards:
            return False
        fav_card = sorted(self.cards, key=lambda x: [-x.balance, -x.limit])[0]
        # выбирается карта в первую очередь с наибольшим балансом, затем с наибольшим лимитом
        if fav_card.spend(cost):
            print(f"{self} have just bought the {product} for the price of {cost}.")
            return True
        return False

    def make_saving_account(self, rate_plan: float, income=0):
        if income < 0:
            print("You're dumb!")
            return None
        if not self.cards:
            return None
        fav_card = sorted(self.cards, key=lambda x: [-x.balance, -x.limit])[0]
        if fav_card.spend(income):
            s = SavingAccount(rate_plan, income)
            self.sa += [s]
            print(f'{self} made a {s}')
            return None
        print('Failed to create a savings account')
        return None

    def get_money_from_sa(self, summ):
        if summ < 0:
            return None
        if not self.sa:
            print(f'{self} have no saving account')
            return None
        fav_sa: SavingAccount
        fav_sa = sorted(self.sa, key=lambda x: -x.balance)[0]
        if fav_sa.transfer(summ):
            fav_card: Card
            fav_card = sorted(self.cards, key=lambda x: x.balance)[0]
            fav_card.add_money(summ)
            print(f'{self} transfered {summ} from {fav_sa} to {fav_card}')
            return None
        print('transfer unsuccessful')
        return None

    def add_money_to_sa(self, summ):
        if summ < 0:
            return None
        if not self.sa:
            print(f'{self} have no saving account')
            return None
        fav_card: Card
        fav_card = sorted(self.cards, key=lambda x: -x.balance)[0]
        if fav_card.spend(summ):
            fav_sa: SavingAccount
            fav_sa = sorted(self.sa, key=lambda x: x.balance)[0]
            fav_sa.add_money(summ)
            print(f'{self} transfered {summ} from {fav_card} to {fav_sa}')
            return None
        print('transfer unsuccessful')
        return None


class Adult(Person):
    def __init__(self, first_name: str, last_name: str, cards: list, ch: list) -> None:
        super().__init__(first_name, last_name, cards)
        self.ch = ch
        self.cash = 0.0
        self.ia = []

    @staticmethod
    def from_json(data: dict):
        return Adult(data.get("first_name"),
                     data.get("last_name"),
                     [Card.from_json(card) for card in data.get("cards")],
                     [Child.from_json(cild) for cild in data.get("children")])  # опечаталась, не стала исправлять

    def get_salary(self, summ):
        fav_card = sorted(self.cards, key=lambda x: x.balance)[0]
        fav_card.add_money(summ)
        print(f'{self} got salary')
        return None

    def take_cash(self, summ: float):
        if not self.cards:
            return None
        fav_card = sorted(self.cards, key=lambda x: -x.balance)[0]  # выбирается карта с наибольшим балансом
        if fav_card.spend(summ):
            self.cash += summ
            print(f'{self} withdrew {summ}')
            return None
        print('Cash withdrawal failed')
        return None

    def give_cash_to_children(self):
        if not self.ch:
            return None
        if not self.cash:
            return None
        fav_child = sorted(self.ch, key=lambda x: x.cash)[0]  # теперь родитель дает деньги не всем детям, а ребенку
        # с наименьшим количеством налички
        fav_child.take_cash_from_parent(self.cash)
        print(f'{self} gave {fav_child} {self.cash}')
        self.cash = 0
        return None

    def make_investment_account(self, income: float):
        if income < 0:
            print("You're dumb!")
            return None
        if not self.cards:
            return None
        fav_card = sorted(self.cards, key=lambda x: [-x.balance, -x.limit])[0]
        if fav_card.spend(income):
            i = InvestmentAccount(income)
            self.ia += [i]
            print(f'{self} made an {i}')
            return None
        print('Failed to create an investment account')
        return None

    def make_required_payment(self, name: str, summ: float, num: int):
        if not self.cards:
            return None
        fav_card = self.cards[num]
        fav_card.create_required_payment(name, summ)
        print(f'{self} made a required payment')
        return None

    def pay_all_req(self):
        if not self.cards:
            return None
        for c in self.cards:
            ks = c.reqpaym.keys()
            if not ks:
                continue
            for k in ks:
                c.pay_req_paym(k)
        print(f'{self} payed all required payments')
        return None

    def pay_one_req(self, num: int, name: str):  # мы выбираем номер карты в списке карт
        fav_card: Card
        fav_card = self.cards[num]
        fav_card.pay_req_paym(name)
        print(f'{self} payed "{name}" required payment')
        return None

    def transfer(self, summ: float, card_num: str):
        if not self.cards:
            return None
        other_card = search_card(card_num)
        if not other_card:
            return None
        fav_card = sorted(self.cards, key=lambda x: -x.balance)[0]
        if fav_card.spend(summ):
            other_card.add_money(summ)
            print('Transfer successful')
            return None
        print('Transfer unsuccessful')
        return None

    def get_money_from_ia(self, summ):
        if summ < 0:
            return None
        if not self.ia:
            print(f'{self} have no saving account')
            return None
        fav_ia: InvestmentAccount
        fav_ia = sorted(self.ia, key=lambda x: -x.balance)[0]
        if fav_ia.transfer(summ):
            fav_card: Card
            fav_card = sorted(self.cards, key=lambda x: x.balance)[0]
            fav_card.add_money(summ)
            print(f'{self} transfered {summ} from {fav_ia} to {fav_card}')
            return None
        print('transfer unsuccessful')
        return None

    def add_money_to_ia(self, summ):
        if summ < 0:
            return None
        if not self.ia:
            print(f'{self} have no saving account')
            return None
        fav_card: Card
        fav_card = sorted(self.cards, key=lambda x: -x.balance)[0]
        if fav_card.spend(summ):
            fav_ia: InvestmentAccount
            fav_ia = sorted(self.ia, key=lambda x: x.balance)[0]
            fav_ia.add_money(summ)
            print(f'{self} transfered {summ} from {fav_card} to {fav_ia}')
            return None
        print('transfer unsuccessful')
        return None


class Child(Person):
    def __init__(self, first_name: str, last_name: str, cards: list, age: int) -> None:
        super().__init__(first_name, last_name, cards)
        self.age = age
        self.cash = 0.0

    @staticmethod
    def from_json(data: dict):
        return Child(
            data.get("first_name"),
            data.get("last_name"),
            [Card.from_json(card) for card in data.get("cards")],
            data.get("age")
        )

    def __str__(self) -> str:
        return super().__str__() + f" {self.age} y. o."

    def take_cash_from_parent(self, summ: float) -> None:
        self.cash += summ
        print(f'{self} took cash')

    def add_cash(self):
        if not self.cards:
            return None
        if not self.cash:
            return None
        fav_card = sorted(self.cards, key=lambda x: x.balance)[0]  # выбирается карта с наименьшим балансом
        fav_card.add_money(self.cash)
        print(f'{self} added cash on {fav_card}')


if __name__ == "__main__":
    ad_ex = {"first_name": "Igor", "last_name": "Sarpinsky",
             "cards": [{"number": "2200887123461122", "balance": 9000000.9},
                       {"number": "2207694123437842", "balance": 888884.9}],
             "children": [{"first_name": "Anastasia", "last_name": "Sarpinskaya",
                           "cards": [{"number": "2130887123479122", "balance": 909, "limit": 600},
                                     {"number": "2075687129823122", "balance": 1500, "limit": 300}], "age": 18}]}
    adult_example = Adult.from_json(ad_ex)
    child_example: Child
    child_example = adult_example.ch[0]
    print(adult_example)
    print(child_example)
    adult_example.buy('milk', 10.8)
    child_example.buy("jacket", 1110.0)
    adult_example.buy('mansion', 345678987654.8)
    child_example.buy("car", 4345678876.0)
    adult_example.make_saving_account(20, 88)
    child_example.make_saving_account(11, 100)
    adult_example.get_money_from_sa(60)
    child_example.get_money_from_sa(70)
    adult_example.add_money_to_sa(30)
    child_example.add_money_to_sa(30)
    adult_example.get_salary(999999999)
    adult_example.take_cash(70000)
    adult_example.give_cash_to_children()
    child_example.add_cash()
    adult_example.make_investment_account(8888)
    adult_example.get_money_from_ia(6000)
    adult_example.add_money_to_ia(2000)
    adult_example.make_required_payment('connection', 88, 1)
    adult_example.pay_all_req()
    adult_example.pay_one_req(1, 'connection')
    adult_example.transfer(1000, '3570363825074491')  # берем номер карты из нашего файла
