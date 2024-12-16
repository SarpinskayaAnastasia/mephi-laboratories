import json
from persons import Person, Adult, Child
from cards import Card
from income_accounts import SavingAccount, InvestmentAccount

with open('people_cards.json') as js:
    data = json.load(js)

dbadults = [Adult.from_json(a) for a in data]
dbchildren = []
for a in dbadults:
    dbchildren.extend(a.ch)
cards = []
num_cards = []
for p in dbchildren + dbadults:
    cards.extend(p.cards)
    num_cards.extend([c.number for c in p.cards])
dbcards = {obj: state for obj, state in zip(num_cards, cards)}

if __name__ == "__main__":
    example = dbadults[2]
    print(example)
    example.make_saving_account(8.0, 7)
    example.get_money_from_ia(9)
    example.get_money_from_sa(6)
    example.make_investment_account(30)
    example.get_money_from_ia(12)
