import json


class Card:
    def __init__(self, number: str, balance: float, limit=float('inf')) -> None:
        # у взрослой карты лимит все-таки есть, но он бесконечный
        self.number = number
        self.balance = balance
        self.limit = limit

    def __str__(self) -> str:
        if self.limit == float('inf'):
            return f"Card's number: {self.number}\nBalance: {self.balance}"
        else:
            return f"Children card's number: {self.number}\nBalance: {self.balance}\nLimit: {self.limit}"

    def spend(self, summ: float) -> bool:
        if (summ <= self.balance) and (summ <= self.limit):
            self.balance -= summ
            return True
        return False

    def deposit(self, summ: float) -> None:
        self.balance += summ


class Person:
    def __init__(self, first_name: str, last_name: str, cards: list) -> None:
        self.fn = first_name
        self.ln = last_name
        self.cards = cards

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


class Adult(Person):
    def __init__(self, first_name: str, last_name: str, cards: list, ch: list) -> None:
        super().__init__(first_name, last_name, cards)
        self.ch = ch

    def give_money_to_children(self, summ: float):
        if not self.ch:
            return None
        if not self.cards:
            return None
        fav_card = sorted(self.cards, key=lambda x: -x.balance)[0]  # выбирается карта с наибольшим балансом
        if fav_card.spend(summ):
            gift = summ / len(self.ch)  # взрослый любит всех своих детей, потому он дает деньги всем поровну)
            for c in self.ch:
                c.take_money_from_parent(gift)


class Child(Person):
    def __init__(self, first_name: str, last_name: str, cards: list, age: int) -> None:
        super().__init__(first_name, last_name, cards)
        self.age = age

    def __str__(self) -> str:
        return super().__str__() + f" {self.age} y. o."

    def take_money_from_parent(self, summ: float) -> None:
        if not self.cards:
            return None
        fav_card = sorted(self.cards, key=lambda x: x.balance)[0]  # выбирается карта с наименьшим балансом
        fav_card.deposit(summ)


def dc_to_card(d: dict) -> Card:
    if "limit" not in d.keys():
        return Card(d["number"], d["balance"])
    else:
        return Card(d["number"], d["balance"], d["limit"])


def dch_to_child(d: dict) -> Child:
    c = [dc_to_card(i) for i in d["cards"]] if d["cards"] else []
    return Child(d["first_name"], d["last_name"], c, d["age"])


def da_to_adult(d: dict) -> Adult:
    c = [dc_to_card(i) for i in d["cards"]] if d["cards"] else []
    ch = [dch_to_child(i) for i in d["children"]] if d["children"] else []
    return Adult(d["first_name"], d["last_name"], c, ch)


with open('people_cards.json', 'r') as js:
    data = json.load(js)
    persons = [da_to_adult(i) for i in data]

ex_ad = persons[2]
print(ex_ad, '\n---------------')
ex_ch = ex_ad.ch[0]
print(ex_ch, '\n---------------')

ex_ad.buy("milk", 10.8)
print('---------------')
ex_ch.buy("jacket", 588.8)
print('---------------')
print('###############')
print('---------------')

ex_ad.buy("apartments", 10000000.0)
ex_ch.buy("car", 5000000.0)
# ничего не выведется

print(*ex_ad.cards, sep='\n---------------\n')
print('---------------')
print(*ex_ch.cards, sep='\n---------------\n')
print('---------------')
ex_ad.give_money_to_children(50.0)
print(*ex_ad.cards, sep='\n---------------\n')
print('---------------')
print(*ex_ch.cards, sep='\n---------------\n')
