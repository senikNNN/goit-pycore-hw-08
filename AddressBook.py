from collections import UserDict
from re import fullmatch
from datetime import datetime, timedelta

__all__ = ['AddressBook', 'Record', 'Name', 'Phone', 'Birthday', 'get_upcoming_birthdays',
           'IncorrectNameExeption', 'IncorrectPhoneExeption', 'IncorrectDateFormat']

class IncorrectNameExeption(Exception):
    pass

class IncorrectPhoneExeption(Exception):
    pass

class IncorrectDateFormat(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if value:
            self.value = value
        else:
            raise IncorrectNameExeption
    
    def __str__(self):
        return self.value

class Phone(Field):
    def __init__(self, value):
        if fullmatch(r"^\d{10}$", value):
            self.value = value
        else:
            raise IncorrectPhoneExeption
    
    def __str__(self):
        return self.value

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise IncorrectDateFormat

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))
    
    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        for i in range(len(self.phones)):
            if self.phones[i] == old_phone.value:
                self.phones[i] = new_phone.value
    
    def find_phone(self, phone: str):
        for element in self.phones:
            if element.value == phone:
                return phone
        return None

    def remove_phone(self, phone: str):
        for element in self.phones:
            if element.value == phone:
                self.phones.remove(element)
    
    def add_birthday(self, birthday: str):
        if birthday:
            self.birthday = Birthday(birthday)

    def edit_birthday(self, new_birthday: datetime):
        self.birthday = new_birthday
    
    def remove_birthday(self):
        self.birthday = None

class AddressBook(UserDict):
    def show_all(self):
        for name, record in self.data.items():
            for phone in record.phones:
                print(f"{name}: {phone.value} {record.birthday}")

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def delete(self, name: str):
        self.data.pop(name)
    
    def find(self, name: str) -> Record:
        finded_record = Record(name)
        for phone in self.data[name].phones:
            finded_record.add_phone(phone.value)
        return finded_record

def get_upcoming_birthdays(book: AddressBook) -> AddressBook:
        """
            Takes a AddressBook of users and their birthdays and returns a AddressBook of users and dates, 
            when they should be congratulated on their birthdays for the next seven days.
        """
        weeklong_celebrations = AddressBook()
        control_day = datetime.today().date()
        last_checked_day = control_day + timedelta(days=7)
        for user in book:
            if  book[user].birthday:
                day = book[user].birthday.value.day
                month = book[user].birthday.value.month
            user_birthday = datetime(year=datetime.now().year, month=int(month), day=int(day)).date()

            is_a_birthday_this_week = user_birthday >= control_day and user_birthday < last_checked_day
            if is_a_birthday_this_week:
                is_birthday_falls_on_a_weekend = user_birthday.weekday() == 5 or user_birthday.weekday() == 6
                if is_birthday_falls_on_a_weekend:
                    delayed_user_birthday = user_birthday + timedelta(days=7 - user_birthday.weekday())
                    #weeklong_celebrations.append({"name": user["name"], "birthday": delayed_user_birthday})
                    weeklong_celebrations.add_record(book[user].edit_birthday(delayed_user_birthday))
                else:
                    weeklong_celebrations.add_record(book[user])      
        return weeklong_celebrations