# Klasa BankAccount, reprezentujaca konto bankowe (nie kredytowe - saldo musi byc nieujemne)
# Dbamy o zalozenie nieujemnosci we wszystkich metodach, oraz rzucamy wyjatek przy
# podejrzanych operacjach (np. wybierania ujemnej kwoty z konta)

class BankAccount:
    def __init__(self, number, balance=0):
        if balance < 0:
            raise ValueError("Cannot create an account with negative balance.")
        self.number = number
        self.balance = balance

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Account number {}: cannot deposit a negative amount.".format(self.number))
        self.balance += amount

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Account number {}: cannot withdraw a negative amount.".format(self.number))
        if amount > self.balance:
            raise ValueError("Account number {}: cannot withdraw {} (current balance: {})".format(self.number, amount, self.balance))
        self.balance -= amount

    def merge_to(self, other_account):
        n = self.balance
        self.withdraw(n)
        other_account.deposit(n)

        # z taka implementacja jest problem, gdy self i other_account jest jednym obiektem:
        # other_account.deposit(self.balance)
        # self.balance = 0
        # jak sprawdzic, czy self i other_account to to samo konto?
        # 1. self.number == other_account.number, przy zalozeniu, ze numery sa unikalne
        # 2. self is other_account - porownuje tozsamosc obiektow (nie rownosc)
        # 3. id(self) == id(other_account) - porownuje unikalne, "prawdziwe" id

    def get_description(self): # zamiast __str__
        return "Account number {}, balance: {}".format(self.number, self.balance)


if __name__ == "__main__":
    account = BankAccount("1234-BANK-0000", 10000)
    print(account.get_description()) # 1
    account.deposit(500)
    print(account.get_description()) # 2
    account.withdraw(8000)
    print(account.get_description()) # 3

    another_account = BankAccount("9999-BANK-0000")
    print(another_account.get_description()) # 4

    account.merge_to(another_account)
    print(account.get_description()) # 5
    print(another_account.get_description()) # 6
    # another_account.withdraw(3000)
