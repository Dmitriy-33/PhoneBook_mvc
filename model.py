from dataclasses import dataclass
import json
import re


@dataclass
class Contact:

    name: str | None = None
    number: str | None = None
    comment: str | None = None


    def validation_name(self) -> str:
        """Валидация введённого имени."""
        if not self.name:
            return 'Имя не может быть пустым!'

        return 'ok'


    def validation_number(self) -> str:
        """Валидация введённого номера."""
        if not self.number:
            return '\nВведён не корректный номер!'

        return 'ok'


class PhoneBook:

    def __init__(self, file_path):
        self.file_path = file_path


class ReadFile:

    def __init__(self, file_path):
        self.file_path = file_path


    def load_phonebook(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)


class SaveData:

    def __init__(self, file_path, data):
        self.file_path = file_path
        self.data = data

    def save_phonebook(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)


def clear_number(number: str) -> str:
    """Оставляем в номере только цифры."""
    return re.sub(r'\D','',number)


def contact_list(phonebook: dict, key: str, data: str) -> list:
    """Создание списка найденных контактов."""
    result = list(row for row in phonebook["contacts"] if data.upper() in str(row[key]).upper())
    return result


def get_name_key(param: int) -> str:
    """Получение имени ключа"""
    match param:
        case 1:
            return "name"
        case 2:
            return "number"
        case 3:
            return "comment"


def search_name(phonebook: dict, name: str) -> list:
    """Поиск по имени."""
    return contact_list(phonebook, get_name_key(1), name)


def search_number(phonebook: dict, number: str) -> list:
    """Поиск по номеру."""
    return contact_list(phonebook, get_name_key(2), clear_number(number))


def search_comment(phonebook: dict, comment: str) -> list:
    """Поиск по комментарию."""
    return contact_list(phonebook, get_name_key(3), comment)


def search_general(phonebook: dict, value: str) -> list:
    """Общий поиск."""
    list_name = contact_list(phonebook, 'name', value)
    list_number = contact_list(phonebook, 'number', value)
    list_comment = contact_list(phonebook, 'comment', value)
    all_list = list_name + list_number + list_comment

    result = list({l['id']: l for l in all_list}.values())

    return result


def find_contact(phonebook: dict, choice: str, value: str) -> list | None:
    """Поиск контактов."""
    if choice == "1":
        return search_name(phonebook,value)
    elif choice == "2":
        return search_number(phonebook,value)
    elif choice == "3":
        return search_comment(phonebook,value)
    elif choice == "4":
        return search_general(phonebook,value)


def add_contact(phonebook: dict, contact: Contact) -> dict:
    """Добавление нового контакта."""
    if not len(phonebook["contacts"]):
        id = 1
    else:
        list_id = list()
        for row in phonebook["contacts"]:
            list_id.append(row.get("id"))
            list_id.sort()
            id = list_id[-1]+1

    data = {"id": id, "name": contact.name, "number": int(contact.number), "comment": contact.comment}
    phonebook["contacts"].append(data)
    return phonebook


def delete_contact(phonebook: dict, delete_contact_id: str) -> dict:
    """Удаление контакта."""
    phonebook["contacts"] = [row for row in phonebook["contacts"] if row["id"] != delete_contact_id]
    return phonebook

def edit_contact(phonebook: dict, edit_contact_id: str, field_id: str, new_value: str) -> dict:
    """Изменение данных контакта"""
    key = get_name_key(int(field_id))

    for index, row in enumerate(phonebook["contacts"]):
        if row.get("id") == edit_contact_id:
            phonebook["contacts"][index][key] = new_value

    return phonebook