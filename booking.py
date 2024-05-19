import json
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Union

from utils.customer import Customer
from utils.parsers import integer_input_parser
from utils.parsers import is_valid_choice
from utils.parsers import string_input_parser
from utils.utils import gen_otp
from utils.utils import sender


@dataclass
class MenuConfiguration:
    width: int = 55

    def construct_menucard(self, menu: List[Dict[str, Union[str, int]]]):
        message = "This is our menu\n"
        upper_score = "\u203e"
        # table header printing line here
        message += (
            f"{'_' * self.width}\n" f"{'Item No.':^10}{'Items':^35}{'Price £':<5}\n" f"{upper_score * self.width}\n"
        )
        for index, dish in enumerate(menu, 1):
            message += f"{index:^10}{dish['Items']:^35}{dish['Price']:<5}\n"

        message += f"{'_' * self.width}"
        print(message)


@dataclass
class ChoiceValidator:
    choices: dict

    def is_valid_choice(self, choice):
        return choice.casefold() in list(map(str.casefold, self.choices.values()))


@dataclass
class ChoiceConfiguration:
    width: int = 55
    choice_help_area: int = field(init=False)
    choice_char_area: int = field(init=False)

    def __post_init__(self):
        self.choice_help_area = self.width - 6
        self.choice_char_area = 0

    def construct_choice_table(self, choices: Dict[str, str], title):
        """
        :param choices:
            dict containing prompt and options
        :param title: title for the selection message
        :return:
        """
        message = f"{'_'*self.width}\n" f"{title:^{self.width}}\n" f"{'_'*self.width}\n"

        for choice_help, choice_char in choices.items():
            choice_help_formatted = f"{choice_help} - Type"
            choice_char_formatted = f"'{choice_char}'"
            message += f"To {choice_help_formatted:.<{self.choice_help_area}}{choice_char_formatted:.>{self.choice_char_area}}\n"

        print(message)


# app logic and function codes are in the class of booking system
class BookingSystem:
    def __init__(self, menu: List[Dict[str, Union[str, int]]], customer: Optional[Customer] = None):
        self.menu = menu
        self._customer = customer
        self.menu_configuration = MenuConfiguration()
        self.choice_configuration = ChoiceConfiguration()

    @property
    def customer(self):
        if not self._customer:
            self._customer = Customer.from_cli_input()
        return self._customer

    @customer.setter
    def customer(self, customer: Customer) -> bool:
        if not isinstance(customer, Customer):
            return False
        self._customer = customer
        return True

    # command line welcome message, display menu card and call dish selector
    def wishinghim(self):
        print("\n Hey," + self.customer.name + "\n Welcome to our Restaurant \n")
        self.showMenucard()
        self.main_menu()

    def showMenucard(self):
        self.menu_configuration.construct_menucard(self.menu)

    def main_menu(self):
        print("current total: " + str(self.currentRateItems()) + "\u00a3")
        choices = {
            "select dish": "S",
            "edit order": "E",
            "complete order": "K",
            "edit email": "M",
        }
        self.choice_configuration.construct_choice_table(
            choices=choices, title="The above menu can be used to place your order"
        )
        choice_validator = ChoiceValidator(choices=choices)
        choice = string_input_parser("input choice: ", validator=choice_validator.is_valid_choice)
        if choice == "M" or choice == "m":
            self.editEmail()
        elif choice == "E" or choice == "e":
            self.editList()
        elif choice == "S" or choice == "s":
            self.selectDishes()
        elif choice == "K" or choice == "k" and self.toCompleteOrder():
            self.finalSltDishs()

    # Edit option after ordered items and any corrections
    def editList(self):
        # Showing ordered Items this codes.
        for orderItem in self.customer.items:
            print(orderItem)
        print("_______________________________________ \n editor is on \n _______________________________________")
        editKey = int(input("Enter your want to edit Serial No: "))
        if editKey <= len(self.customer.items):
            print("if you want to delete item type--'D' \n if you want to edit quality of item type-- 'Q'")
            choice = input("Type your Choice: ")
            if choice == "D" or choice == "d":
                self.customer.items.pop(editKey - 1)
                print("sucessfully deleted!")
            if choice == "Q" or choice == "q":
                quantity = int(input("Enter your Change Quantity of Dish: "))
                self.customer.items[editKey - 1]["Quantity"] = quantity

                print("sucessfully changed Quantity! \n_______________________________________")

    def selectQuantity(self) -> int:
        try:
            quantity = int(input("Enter Quantity of Dish: "))
            return quantity
        except ValueError:
            print("Please enter number not a word!")
            return self.selectQuantity()

    # Select Dishes by serial number , ordering and mentioning quantiy.
    def selectDishes(self):
        for orderItem in self.customer.items:
            print(orderItem)
        print("_______________________________________ \n Select your Dish \n_______________________________________")

        notFinished = True
        while notFinished:
            sltDishId = integer_input_parser("Enter Item No. : ")
            if sltDishId <= len(self.menu):
                selDish = self.menu[sltDishId - 1]
                quantity = self.selectQuantity()
                selDish["Quantity"] = quantity
                self.customer.items.append(selDish)
                print("sucessfully registered \n_______________________________________")
                notFinished = False
            else:
                print("Invalid Item")
                notFinished = True

    # This outputs current list ordered pfrice
    def currentRateItems(self) -> int:
        total = 0
        for items in self.customer.items:
            peritem = items["Price"] * items["Quantity"]
            total += peritem
        return total

    # completiion of order and send to final process of billing
    def toCompleteOrder(self):
        print("Is your order complete? \n To Finish type --'Y' \n To continue type--'N'")
        confirmation = input("Type you decison: ")
        if confirmation == "Y" or confirmation == "y":
            print("Orders are registered!")
            return True
        if confirmation == "N" or confirmation == "n":
            return False

    # aggregate the finalised items
    def finalisedItems(self) -> List[Dict[str, int]]:
        return self.customer.items

    # Editing frist entered mail and it will otp authentication process
    def editEmail(self):
        print("_______________________________________ \n Edit email ID \n_________________________________")
        changeEmail = input("Enter your new Email ID: ")
        Otp = gen_otp()
        message = "it is your OTP: " + str(Otp)
        sender(changeEmail, "verification for change new email ID", message)
        verify = input("Enter you Otp number recieved in mail: ")
        if verify == Otp:
            self.customer.email = changeEmail

    # Final showing of ordered list and here can delete items and go to email process
    def finalSltDishs(self):
        count = 0
        print(
            "________________________________________________ \n Item No. --*-- Items--------*-- Price -------*-- Quantity"
        )
        for orderItem in self.customer.items:
            S, Is, Pe, Qy = (
                str(count + 1),
                orderItem["Items"],
                str(orderItem["Price"]),
                str(orderItem["Quantity"]),
            )
            print(" " + S + " --*-- " + Is + "--------*-- " + Pe + "\u00a3 -------*-- " + Qy + "-Qty")
            count += 1
        print("********* total amount:" + str(self.currentRateItems()) + "\u00a3 ******")
        print("\n Delivery address:" + str(self.customer.address) + "\n")
        waittoconfirm = True
        while waittoconfirm:
            print(
                "_____________________________________________________\n please confirm your email ID '"
                + self.customer.email
                + "' as bill and payment option will be sent via email. \n To edit email id type--'M'",
                " \n To edit items type--'E' \n Show Ordered list again type--'S' \n Confirm Your final Order type--'O' ",
            )
            choice = input("Enter your choice: ")
            if choice == "M" or choice == "m":
                self.editEmail()
            elif choice == "E" or choice == "e":
                self.editList()
            elif choice == "O" or choice == "o":
                self.finalisedItems()
                waittoconfirm = False
            elif choice == "S" or choice == "s":
                count = 0
                for orderItem in self.customer.items:
                    S, Is, Pe, Qy = (
                        str(count + 1),
                        orderItem["Items"],
                        str(orderItem["Price"]),
                        str(orderItem["Quantity"]),
                    )
                    print(" " + S + " --*-- " + Is + "--------*-- " + Pe + "\u00a3 -------*-- " + Qy + "-Qty")
                    count += 1
                print("total price: " + str(self.currentRateItems()) + "\u00a3")
            elif choice == "D" or choice == "d":
                exit()


if __name__ == "__main__":
    session = True
    menu = None
    with open("menucard.json") as json_file:
        menu = json.load(json_file)

    if not menu:
        raise FileNotFoundError("No file was found for the menu assert that menucard.json exists in the directory")

    booking_system = BookingSystem(menu)
    while session:
        choice_configuration = ChoiceConfiguration()
        choices = {"order food": "Y", "quit": "Q"}
        choice_validator = ChoiceValidator(choices=choices)
        choice_configuration.construct_choice_table(choices=choices, title="welcome to online booking system")
        choice: str = string_input_parser("Type Your Choice:", validator=choice_validator.is_valid_choice)

        if choice.casefold() == "y".casefold():
            customer = Customer.from_cli_input()
            booking_system.customer = customer
            booking_system.wishinghim()

        if choice.casefold() == "n".casefold():
            exit()
