from enum import Enum

class ParameterError(Exception):
    pass

class SystemError(Exception):
    pass

class Card(object):

    def __init__(self, pin, account_numbers):
        self._pin = pin
        self._account_numbers = account_numbers
    
    def check_pin(self, pin):
        return self._pin == pin

    def get_accounts(self):
        return self._account_numbers
    
    def has_account(self, account_id):
        return account_id in self._account_numbers

    @property
    def account_number(self):
        return self._account_numbers

class Account(object):

    def __init__(self, account_number, initial_balance):
        self._account_number = account_number
        self._balance = initial_balance

    @property
    def account_number(self):
        return self._account_number

    def get_balance(self):
        return self._balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise ParameterError("Cannot deposit negative or zero amount")
        self._balance += amount
        return self._balance
    
    def withdrawal(self, amount):
        if amount <= 0:
            raise ParameterError("Cannot withdrawal negative or zero amount")
        if self._balance < amount:
            raise ParameterError("Cannot withdrawal more money than balance")
        self._balance -= amount
        return self._balance


class Bank(object):

    def __init__(self):
        self._account_info = dict()
        self._account_info_uuid = 0
    
    def get_account_uuid(self):
        self._account_info_uuid += 1
        return self._account_info_uuid

    def add_account(self, account):
        self._account_info[account.account_number] = account

    def get_account(self, account_number):
        if not account_number in self._account_info:
            raise SystemError(
                "Cannot find account info: {0}".format(account_number))
        return self._account_info[account_number]

class ATMState(Enum):
    CARD_NOT_PRESENT = 0
    CARD_PRESENT_AND_NOT_AUTHENTICATED = 1
    CARD_PRESENT_AND_AUTHENTICATED = 2
    CARD_PRESENT_AND_ACCOUNT_SELECTED = 3

class ATM(object):

    def __init__(self, bank):
        self._bank = bank
        self._state = ATMState.CARD_NOT_PRESENT
        self._card = None
        self._account = None

    def insert_card(self, card):
        if self._state != ATMState.CARD_NOT_PRESENT:
            raise SystemError("Card already present")
        print("card inserted")
        self._card = card
        self._state = ATMState.CARD_PRESENT_AND_NOT_AUTHENTICATED
        self._account = None
    
    def authenticate_card_with_pin(self, pin):
        if self._state != ATMState.CARD_PRESENT_AND_NOT_AUTHENTICATED:
            raise SystemError("Card not present")

        if not self._card.check_pin(pin):
            raise SystemError("Could not authentication with given pin")
    
        print("card authenticated")
        self._state = ATMState.CARD_PRESENT_AND_AUTHENTICATED

    def list_accounts_on_card(self):
        if self._state != ATMState.CARD_PRESENT_AND_AUTHENTICATED:
            raise SystemError("Card not authenticated")
        
        print("List of accounts: {0}".format(self._card.get_accounts()))

    def select_account_on_card(self, account_id):
        if self._state != ATMState.CARD_PRESENT_AND_AUTHENTICATED:
            raise SystemError("Card not authenticated")
        
        if not self._card.has_account(account_id):
            raise SystemError("Tried to use account not existing on card")

        self._account = self._bank.get_account(account_id)        
        print("select account: {0}".format(account_id))
        self._state = ATMState.CARD_PRESENT_AND_ACCOUNT_SELECTED

    def withdrawal(self, amount):
        if self._state != ATMState.CARD_PRESENT_AND_ACCOUNT_SELECTED:
            raise SystemError("Not authenticated")
        
        print("Account {0} balance after withdrawal {1}: {2}".format(
            self._account.account_number,
            amount,
            self._account.withdrawal(amount)))
    
    def deposit(self, amount):
        if self._state != ATMState.CARD_PRESENT_AND_ACCOUNT_SELECTED:
            raise SystemError("Not authenticated")
        
        print("Account {0} balance after adding {1}: {2}".format(
            self._account.account_number,
            amount,
            self._account.deposit(amount)))

    def get_balance(self):
        if self._state != ATMState.CARD_PRESENT_AND_ACCOUNT_SELECTED:
            raise SystemError("Not authenticated")
        
        print("Account {0} balance: {1}".format(
            self._account.account_number,
            self._account.get_balance()))

    def eject_card(self):
        self._card = None
        self._account = None
        self._state = ATMState.CARD_NOT_PRESENT

def test():
    USE_USER_INPUT = True
    bank = Bank()
    bank.add_account(Account(bank.get_account_uuid(), 10))
    bank.add_account(Account(bank.get_account_uuid(), 20))
    card1 = Card(1234, [1])
    card2 = Card(5555, [2])
    atm = ATM(bank)

    test_inputs = [
        "add_card card1",
        "add_card card2",
        "authenticate 1",
        "withdrawal 1",
        "authenticate 1234",
        "list_account",
        "select_account 999",
        "select_account 1",
        "get_balance",
        "withdrawal 1",
        "deposit 1",
        "withdrawal 22",
        "eject 0",
        "add_card card1",
        "get_balance",
        "authenticate 1234",
        "get_balance",
        "eject 0",
        "add_card card2",
        "authenticate 5555",
        "select_account 2",
        "get_balance",
    ]

    while True:
        try:
            if USE_USER_INPUT:
                user_input = input()
            else:
                if len(test_inputs) == 0:
                    break
                user_input = test_inputs[0]
                del test_inputs[0]

            print("Userinput: ", user_input)
            command = user_input
            if user_input.find(" ") >= 0:
                command, action = user_input.split(" ")
            if command == "add_card":
                # XXX: do not use eval in production code
                atm.insert_card(eval(action))
            elif command == "authenticate":
                atm.authenticate_card_with_pin(int(action))
            elif command == "withdrawal":
                atm.withdrawal(int(action))
            elif command == "deposit":
                atm.deposit(int(action))
            elif command == "get_balance":
                atm.get_balance()
            elif command == "list_account":
                atm.list_accounts_on_card()
            elif command == "select_account":
                atm.select_account_on_card(int(action))
            elif command == "eject":
                atm.eject_card()
        except Exception as e:
            print("Got exception: ", str(e))


def main():
    test()

if __name__ == "__main__":
    main()
