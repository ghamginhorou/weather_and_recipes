
def choice_made(choices_list):
    """
    :param choices_list: the list of menu choices. each element is a list with number and description
    :return: the number of the choice that the user has selected if it exists in the menu choices.
    """
    while True:
        option_numbers = []
        print("This is the menu with all services: \n")
        for i in choices_list:
            print(f"{i[0]}. {i[1]}")
            option_numbers.append(i[0])
        choice = input("\nEnter the number of the option you want to select: ")
        if choice in option_numbers:
            return choice
        print(f"\nThe option with number {choice} does not exist.\nPlease enter a valid option number!\n")


def y_or_n_choice(message):
    """
    :return: true or false
    only accepts y or n
    """
    while True:
        choice = input(f"{message} (y/n): ")
        if choice.lower() == "y":
            print()
            return True
        elif choice.lower() == "n":
            print()
            return False
        else:
            print("Please enter y or n.")
