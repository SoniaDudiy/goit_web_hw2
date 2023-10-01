from collections import UserDict
from datetime import datetime
import pickle

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def is_valid_phone(self):
        pass 

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if self.is_valid_phone(new_value):
            self.__value = new_value
        else:
            raise ValueError("Invalid phone number")        

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strtime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Invalid date format. Please use 'YYYY-MM-DD'.")
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        try:
            self.__value == datetime.strptime(new_value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Invalid date format. Please use 'YYYY-MM-DD'.")

class Record:
    def __init__(self, name: str, phones: list, emails: list, birthday: str = None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones]
        self.emails = emails
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phones:
            self.phones.append(phone_number)

    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        return None        

    def delete_phone(self, value):
        phone_to_delete = self.find_phone(value)
        if phone_to_delete:
            self.phones.remove(phone_to_delete)

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone

    def days_to_birthday(self):
        if self.birthday:
            return self.birthday.days_to_birthday()
        return None             

class AddressBook(UserDict):
    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index < len(self.data):
            key = list(self.data.keys())[self._iter_index]    
            value = self.data[key]
            self._iter_index += 1
            return (key, value)
        else:
            raise StopIteration
                
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, value):
        return self.data.get(value)  

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass       

    def search_handler(address_book, data):
        query = ' '.join(data).lower()
        matching_records = address_book.search(query)
        if matching_records:
            result = "Matching records:\n"
            for name, record in matching_records:
                phones = ', '.join([phone.value for phone in record.phones])
                result += f"{name}: {phones}\n"
        else:
            result = "No matching records found"
        return result      

def main():
    address_book = AddressBook()
    address_book.load_from_file("address_book.pkl")

    while True:
        user_input = input(">>> ")
        if not user_input:
            continue
        func, data = command_parser(user_input)
        if not func:
            print("Unknown command. Type 'hello' for available commands.")
        else:
            result = func(address_book, data)
            print(result)
            if func == exit_handler:
                address_book.save_to_file("address_book.pkl")
                break  

def add_handler(address_book, data):
    name = data[0].title()
    phone = data[1]
    record = address_book.find_record(name)
    if record:
        record.add_phone(phone)
        return f"Phone {phone} was added to contact {name}"
    else:
        record = Record(name, [phone], [])
        address_book.add_record(record)
        return f"Contact {name} with phone {phone} was saved"

def change_handler(address_book, data):
    name = data[0].title()
    phone = data[1]
    record = address_book.find_record(name)
    if record:
        record.edit_phone(phone, phone)
        return f"Phone number for contact {name} was changed to {phone}"
    else:
        return "Contact not found"

def phone_handler(address_book, data):
    name = data[0].title()
    record = address_book.find_record(name)
    if record:
        phones = ", ".join([phone.value for phone in record.phones])
        return f"The phone number(s) for contact {name} is/are: {phones}"
    else:
        return "Contact not found"

def show_all_handler(address_book, *args):
    if not address_book.data:
        return "The address book is empty"
    contacts = "\n".join([f"{name}: {', '.join([phone.value for phone in record.phones])}" for name, record in address_book.data.items()])
    return contacts

def exit_handler(address_book, *args):
    return "Good bye!"

def hello_handler(address_book, *args):
    return "How can I help you?"

def command_parser(raw_str: str):  # Парсер команд
    elements = raw_str.split()
    for func, cmd_list in COMMANDS.items():
        for cmd in cmd_list:
            if elements[0].lower() == cmd:
                return func, elements[1:]
    return None, None

    

COMMANDS = {
    add_handler: ["add", "додай", "+"],
    change_handler: ["change", "змінити"],
    phone_handler: ["phone", "телефон"],
    show_all_handler: ["show all", "показати все", "всі контакти"],
    exit_handler: ["good bye", "close", "exit"],
    hello_handler: ["hello"]
}

def main():
    address_book = AddressBook()
    address_book.load_from_file("address_book.pkl")

    while True:
        user_input = input(">>> ")
        if not user_input:
            continue
        func, data = command_parser(user_input)
        if not func:
            print("Unknown command. Type 'hello' for available commands.")
        else:
            result = func(address_book, data)
            print(result)
            if func == exit_handler:
                address_book.save_to_file("address_book.pkl")
                break

if __name__ == "__main__":
    main()