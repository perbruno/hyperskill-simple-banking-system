# Write your code here
import random
import math
import database as db


def log_menu():
    global keep

    option = int(input("1. Create an account \n" +
                       "2. Log into account \n" +
                       "0. Exit\n"))
    card = Card()
    if option == 0:
        keep = False
    elif option == 1:
        card.create_card()
    elif option == 2 and db.is_not_empty():
        card.validate_card()


class Card:

    def __init__(self):
        self.number = None
        self.pin = None

    def luhn_generator(self, number):
        num_list = list(number)
        checksum = 0
        for i in range(len(num_list)):
            num = int(num_list[i])
            if i % 2 == 0:
                num = num * 2 if num < 5 else num * 2 - 9
            checksum += num
        checksum = math.ceil(checksum / 10.0) * 10 - checksum
        return number + str(checksum)

    def card_number_gen(self) -> str:
        luhn_num = 4 * (10 ** 14) + random.randint(0, 10 ** 9 - 1)
        luhn_ = str(luhn_num)
        return self.luhn_generator(luhn_)

    def generate_numbers(self):
        number = self.card_number_gen()
        while number == db.get_data('number', number):
            number = self.card_number_gen()
        self.number = number
        self.pin = f'{random.randint(0, 9999):04}'
        db.insert_item(number=self.number, pin=self.pin)

    def create_card(self):
        self.generate_numbers()
        print("Your card has been created")
        print("Your card number:")
        print(self.number)
        print("Your PIN:")
        print(self.pin)

    def transfer_value(self, card):
        recipient = input("Enter card number:\n")
        if self.luhn_generator(recipient[:-1]) != recipient:
            print("Probably you made a mistake in the card number. Please try again")
        elif not db.get_data('number', recipient):
            print("Such a card does not exist.")
        else:
            amount = int(input("Enter how much money you want to transfer:\n"))

            if db.get_balance(card) < amount:
                print("Not enough money!")
            else:
                db.update_balance(recipient, amount)
                db.update_balance(card, -amount)

    def validate_card(self):
        number = input("Enter your card number:\n")
        pin = input("Enter your PIN:\n")
        if db.get_data('number', number, ['pin', pin]):
            print("You have successfully logged in!")
            global logged
            logged = True
            while logged:
                self.logged_menu(number)
        else:
            print("Wrong card number or PIN!")

    def logged_menu(self, number):
        global logged
        global keep
        option = int(input("1. Balance \n" +
                           "2. Add income \n" +
                           "3. Do transfer \n" +
                           "4. Close account \n" +
                           "5. Log out \n" +
                           "0. Exit\n"))
        if option == 0:
            logged = False
            keep = False

        elif option == 5:
            logged = False

        elif option == 1:
            print(f"Balance: {db.get_balance(number)}")

        elif option == 2:
            db.update_balance(number, int(input("Enter income:\n")))
            print('Income was added!')

        elif option == 3:
            self.transfer_value(number)

        elif option == 4:
            db.close_account(number)
            print("The account has been closed")
            logged = False


def main():
    global keep
    keep = True
    # logged = None

    db.create_table()

    while keep:
        log_menu()
    print("Bye")


main()
