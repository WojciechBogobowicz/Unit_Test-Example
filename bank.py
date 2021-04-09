from bankaccount import BankAccount
from random import randint, seed


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.account_num = 0
        self.used_ibans = []
        with open("iban.txt") as f:
            for line in f:
                line = line.strip()
                bank_id, bank_name = line.split(":")
                if bank_name == self.name:
                    return None
            raise ValueError(f"Cannot find bank named {self.name}")

    def make_account(self, balance=0):
        self.account_num = self.generate_IBAN()
        while self.account_num in self.accounts.keys() or self.account_num in self.used_ibans:
            self.account_num = self.generate_IBAN()
        number = self.account_num
        account = BankAccount(number, balance)
        self.accounts[number] = account
        return account

    def get_account(self, number):
        if number not in self.accounts:
            raise ValueError('No account with number {}'.format(number))
        return self.accounts[number]

    def del_account(self, number):
        if number not in self.accounts.keys():
            raise ValueError('No account with number {}'.format(number))
        del self.accounts[number]
        self.used_ibans.append(number)

    def money_in_the_bank(self):
        return sum([i.balance for i in self.accounts.values()])

    def withdraw_all(self):
        saldo = self.money_in_the_bank()
        for account in self.accounts.values():
            account.withdraw(account.balance)
        return saldo

    def merge_all(self, account):
        account.deposit(self.withdraw_all())

    def move_to(self, other):
        for account in self.accounts.values():
            other.make_account(account.balance)
        self.accounts = {}

    def get_bank_number(self):
        with open("iban.txt") as f:
            for line in f:
                line = line.strip()
                bank_id, bank_name = line.split(":")
                if bank_name == self.name:
                    return bank_id
            raise ValueError(f"Cannot find bank named {self.name}")

    def get_user_number(self):
        user_number = ""
        seed()
        for i in range(16):
            user_number += str(randint(0, 9))
        return user_number

    def add_control_sum(self, iban):
        number = int(iban + "252100")
        number += 98 - number % 97
        number = str(number)
        number = "PL" + number[-2:] + number[:-6]
        return number

    def generate_IBAN(self):
        #https://direct.money.pl/numerkonta/?account_number=54215000003292293856381773
        iban = self.get_bank_number() + self.get_user_number()
        iban = self.add_control_sum(iban)
        return iban


if __name__ == "__main__":
    mbank = Bank("mBank Hipoteczny Spółka Akcyjna")
    bnp = Bank("BNP Paribas Bank Polska Spółka Akcyjna")
    basia = mbank.make_account(100)
    bartek = mbank.make_account(0)
    print(mbank.accounts.values())
    print(bnp.accounts.values())
    mbank.move_to(bnp)
    print(mbank.accounts.values())
    print(bnp.accounts.values())


    """    bank1 = Bank("PL1")
    bank1.make_account(1000)
    bank1.make_account(2000)
    bank2 = Bank("DE2")
    
    account1 = bank1.get_account("PL1-1")
    account2 = bank2.make_account(3000)

    account2.merge_to(account1)
    print(account1.balance)

    """

"""    bank = Bank("cokolwiek")
    bank2 = Bank("szwajcaria")
    acc1 = bank.make_account(1000)
    acc2 = bank.make_account(2000)
    bank.del_account("cokolwiek-2")
    acc3 = bank.make_account(3000)
#    print(bank.money_in_the_bank(), "tyle mamy kasy")
    machlojki = bank2.make_account(0)
  #  bank.merge_all(machlojki)
   # print(machlojki.balance, "tyle ukradlismy")
    #print(bank.money_in_the_bank(), "tyle zostalo ludziom")
    print(bank.accounts, "<- bank")
    print(bank2.accounts, "<- bank2")
    bank.move_to(bank2)
    print("po przejsciu")
    print(bank.accounts, "<- bank")
    print(bank2.accounts, "<- bank2")
"""