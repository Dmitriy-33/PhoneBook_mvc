

def show_main_menu():
    print("\n=== Телефонный справочник ===")
    print("1. Показать все контакты")
    print("2. Добавить контакт")
    print("3. Удалить контакт")
    print("4. Редактировать контакт")
    print("5. Найти контакт")
    print("6. Выйти")


def find_contact_menu():
    print("\n=== Поиск будет производиться по: ===")
    print("1. Имени")
    print("2. Номеру")
    print("3. Комментарию")
    print("4. Общий поиск")
    print("5. Выйти")


def edit_contact_menu():
    print("\n=== Список данных для редактирования: ===")
    print("1. Имя")
    print("2. Номер")
    print("3. Комментарий")


def input_data(message: str):
    return input(message).strip()


def print_message(message: str):
    return print('\n'+message)


def print_contact(contact_list: list):
    """Вывод списка найденных контактов."""
    if not contact_list:
        print_message("Контакт не найден.")
        return
    else:
        for row in contact_list:
            print_message(f"{contact_list.index(row)+1}. {row['name']}: {row['number']} 'Комментрарий:' {row['comment']}")