import json


class Card:
    def __init__(self, number: str, balance: float, limit=float('inf'), children=False) -> None:
        # у взрослой карты лимит все-таки есть, но он бесконечный
        self.number = number
        self.balance = balance
        self.limit = limit
        self.children = children
        self.reqpaym = {}

    @staticmethod
    def from_json(data: dict):
        isch = bool(data.get("limit"))
        return Card(data.get("number"), data.get("balance"), data.get("limit", float('inf')), isch)

    def __str__(self) -> str:
        if self.limit == float('inf'):
            return f"Card's number: {self.number}"
        else:
            return f"Children card's number: {self.number}"

    def spend(self, summ: float) -> bool:
        if (summ <= self.balance) and (summ <= self.limit):
            self.balance -= summ
            print(f'{self} balance decreased by {summ}')
            return True
        print('not enough money')
        return False

    def add_money(self, summ: float) -> None:
        self.balance += summ
        print(f'{self} balance increased by {summ}')
        return None

    def create_required_payment(self, name: str, summ: float):
        if self.children:
            print(f'{self} is children card...')
            return None
        self.reqpaym[name] = summ
        print(f'Payment {name} was created successfully')
        return None

    def pay_req_paym(self, name):
        if not self.reqpaym:
            print('There is no required payment')
        if name not in self.reqpaym.keys():
            print(f'Payment "{name}" is not exist')
            return None
        if self.spend(self.reqpaym[name]):
            print(f'Required payment "{name}" was succeed')
            return None
        print(f'Required payment "{name}" was unsucceed')
        return None


with open("people_cards.json", "r") as file:
    cards = list()
    [cards.extend(x.get("cards")) for x in json.load(file)]
    dbcards = dict([(Card.from_json(x).number, Card.from_json(x)) for x in cards])
    del cards


def search_card(number: str) -> Card or None:
    global dbcards
    m = dbcards.get(number)
    if m:
        if m.children:
            print("Card with this number found, but it kid's")
            return None
        print("Card with this number is found")
        return m
    print("Card with this number isn't found")
    return None


if __name__ == "__main__":
    ad_ex = {"number": "2200887123461122", "balance": 9000000.9}
    adult_example = Card.from_json(ad_ex)
    ch_ex = {"number": "2130887123479122", "balance": 909, "limit": 600}
    child_example = Card.from_json(ch_ex)
    print(adult_example)
    print(child_example)
    adult_example.spend(89)
    adult_example.spend(3456789876543)
    child_example.create_required_payment('sheesh', 88)
    child_example.pay_req_paym('sheesh')
    adult_example.create_required_payment('fuu', 200)
    adult_example.pay_req_paym('fuu')
    adult_example.pay_req_paym('mortgage')
    adult_example.create_required_payment('mortgage', 1234567890123456)
    adult_example.pay_req_paym('mortgage')
    adult_example.add_money(65434567654.66)
    child_example.add_money(2345678909876.99)
