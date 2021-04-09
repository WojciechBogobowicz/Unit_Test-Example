import unittest
from bank import Bank


class TestBank(unittest.TestCase):
    def setUp(self):
        self.mbank = Bank("mBank Hipoteczny Spółka Akcyjna")
        self.mbank_account = self.mbank.make_account(1000)
        self.bnp = Bank("BNP Paribas Bank Polska Spółka Akcyjna")
        self.bnp_account = self.bnp.make_account()

    def test_init(self):
        with self.assertRaises(ValueError):
            t = Bank("test")

    def test_make_account(self):
        acc = self.mbank.make_account()
        self.assertIn(acc.number, self.mbank.accounts.keys())
        with self.assertRaises(ValueError):
            t = self.mbank.make_account(-1)

    def test_get_account(self):
        self.assertIs(self.mbank_account, self.mbank.get_account(self.mbank_account.number))
        with self.assertRaises(ValueError):
            self.mbank.get_account("test")

    def test_del_account(self):
        self.mbank.del_account(self.mbank_account.number)
        self.assertNotIn(self.mbank_account.number, self.mbank.accounts.keys())
        with self.assertRaises(ValueError):
            self.mbank.del_account("test")

    def test_money_in_the_bank(self):
        self.assertEqual(self.mbank.money_in_the_bank(), 1000)
        self.mbank.make_account(9000)
        self.assertEqual(self.mbank.money_in_the_bank(), 10000)

    def test_wirdraw_all(self):
        self.mbank.withdraw_all()
        self.assertEqual(self.mbank.money_in_the_bank(), 0)

    def test_merge_all(self):
        mbank_money = self.mbank.money_in_the_bank()
        bnp_money = self.bnp.money_in_the_bank()
        self.mbank.merge_all(self.bnp_account)
        self.assertEqual(0, self.mbank.money_in_the_bank())
        self.assertEqual(mbank_money + bnp_money, self.bnp.money_in_the_bank())
        self.bnp.merge_all(self.bnp_account)
        self.assertEqual(mbank_money + bnp_money, self.bnp_account.balance)

    def test_move_to(self):
        mbank_balances = [i.balance for i in self.mbank.accounts.values()]
        bnp_banaces = [i.balance for i in self.bnp.accounts.values()]
        balances = mbank_balances + bnp_banaces
        self.mbank.move_to(self.bnp)
        mbank_balances = [i.balance for i in self.mbank.accounts.values()]
        bnp_banaces = [i.balance for i in self.bnp.accounts.values()]
        for i in balances:
            self.assertNotIn(i, mbank_balances)
            self.assertIn(i, bnp_banaces)

    def test_generate_iban(self):
        for i in range(20):
            acc = self.mbank.make_account()
            iban = acc.number
            number = int(iban[4:] + "2521" + iban[2:4])
            self.assertEqual(1, number % 97)
        bank_number = iban[4:12]
        with open("iban.txt") as f:
            for line in f:
                line = line.strip()
                bank_id, bank_name = line.split(":")
                if bank_id == bank_number:
                    self.assertEqual(self.mbank.name, bank_name)
                    break




if __name__ == "__main__":
    unittest.main()
