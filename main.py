import pickle
from AddressBook import *


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def handle_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid number of arguments entered!"
        except KeyError: 
            return "Contact not found."
        except IncorrectPhoneExeption:
            return "Incorrect phone number entered"
        except IncorrectNameExeption:
            return "The username is incorrect"
        except IncorrectDateFormat:
            return "Incorrect date, try the following format: DD.MM.YYYYY."
    return inner

@handle_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@handle_error
def add_contact(args, contacts):
    if len(args) == 2:
        name, phone = args
        birthday = None
    elif len(args) == 3:
        name, phone, birthday = args
    else:
        raise ValueError
    contact = Record(name)
    contact.add_phone(phone)
    contact.add_birthday(birthday)
    contacts.add_record(contact)
    return "Contact added."

@handle_error
def change_contact(args, contacts): 
    if len(args) == 2:
        name, new_birthday = args
        contacts[name].edit_birthday(Birthday(new_birthday))
        return "Contact birthday changed."
    elif len(args) == 3:
        name, old_phone, new_phone = args
        contacts[name].edit_phone(Phone(old_phone), Phone(new_phone))
        return "Contact phone changed."
    else:
        raise ValueError
    
@handle_error
def delete_contact(args, contacts): 
    name = args[0]
    contacts.delete(name)
    return f"Contact {name} deleted"

@handle_error
def add_phone(args, contacts): 
    name, new_phone = args
    contacts[name].add_phone(new_phone)
    return f"For contact {name} added {new_phone}"

@handle_error
def add_birthday(args, contacts): 
    name, new_birthday = args
    contacts[name].edit_birthday(Birthday(new_birthday))
    return "Contact birthday changed."

@handle_error
def show_phone(args, contacts):
    name = args[0]
    if name in contacts:
        all_phones = list()
        for phone in contacts[name].phones:
            all_phones.append(phone.value)
        return f"{name}: {" ".join(all_phones)}"
    else:
        raise KeyError

@handle_error
def show_birthday(args, contacts):
    name = args[0]
    if name in contacts:
        return f"{name}: {contacts[name].birthday}"
    else:
        raise KeyError
    
@handle_error
def birthdays(contacts):
    get_upcoming_birthdays(contacts).show_all()

def show_all(contacts):
    if contacts:
        contacts.show_all()
    else:
        print("Empty...")



def main():
    #contacts = AddressBook()
    contacts = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "del":
            print(delete_contact(args, contacts))
        elif command == "add-phone":
            print(add_phone(args, contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-phone":
            print(show_phone(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "birthdays":
            birthdays(contacts)
        elif command == "all":
            show_all(contacts)
        else:
            print("Invalid command.")
    
    save_data(contacts)


if __name__ == "__main__":
    main()