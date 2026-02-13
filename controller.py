import sys
import view
import model
from json import JSONDecodeError

FILE_NAME = 'phonebook.json'
contact = model.Contact(None,None,None)


def select_contact(contact_list: list[dict], text: str) -> dict:
    view.print_contact(contact_list)
    select_choice = view.input_data(f"{text} (1–{len(contact_list)}): ")

    while model.clear_number(select_choice) == '' or int(select_choice) < 1 or int(select_choice) > len(contact_list):
        view.print_message(f"Неверный выбор. Пожалуйста, введите число от 1 до {len(contact_list)}.")
        select_choice = view.input_data(f"{text} (1–{len(contact_list)}): ")

    selected_contact = contact_list[int(select_choice) - 1]
    return selected_contact


def list_contacts_found(phonebook: list, find_choice: str) -> list[dict] | None:
    if find_choice == "1":
        contact.name = view.input_data("Введите имя: ")
        valid_name = contact.validation_name()

        if valid_name != 'ok':
            view.print_message(valid_name)
        else:
            contact_list = model.find_contact(phonebook, find_choice, contact.name)
    elif find_choice == "2":
        contact.number = view.input_data("Введите номер: ")
        contact.number = model.clear_number(contact.number)
        valid_number = contact.validation_number()

        if valid_number != 'ok':
            view.print_message(valid_number)
        else:
            contact_list = model.find_contact(phonebook, find_choice, contact.number)
    elif find_choice == "3":
        contact.comment = view.input_data("Введите комментарий: ")
        contact_list = model.find_contact(phonebook, find_choice, contact.comment)
    elif find_choice == "4":
        string = view.input_data("Введите данные поиска: ")
        contact_list = model.find_contact(phonebook, find_choice, string)

    return contact_list


def start_app():

    view.show_main_menu()
    choice = view.input_data("Выберите действие (1–6): ")

    phonebook_path = model.PhoneBook(FILE_NAME)

    try:
        reader = model.ReadFile(phonebook_path.file_path)
    except FileNotFoundError:
        view.print_message("Файл не найден!")
        sys.exit()
    except JSONDecodeError:
        view.print_message("Недопустимый формат JSON!")
        sys.exit()

    phonebook = reader.load_phonebook()

    while choice in ["1","2","3","4","5","6"]:

        if choice == "1":
            if not phonebook or not len(phonebook["contacts"]):
                view.print_message("Справочник пуст.")
            else:
                view.print_message("Контакты телефонного справочника:")
                view.print_contact(phonebook['contacts'])
        elif choice == "2":
            contact.name = view.input_data("Введите имя: ")
            contact.number = view.input_data("Введите номер телефона: ")
            contact.comment = view.input_data("Введите комментарий (не обязательно): ")

            valid_name = contact.validation_name()

            contact.number = model.clear_number(contact.number)
            valid_number = contact.validation_number()


            if valid_name != 'ok':
                view.print_message(valid_name)
            elif valid_number != 'ok':
                view.print_message(valid_number)
            else:
                data = model.add_contact(phonebook, contact)
                writer = model.SaveData(phonebook_path.file_path,data)
                writer.save_phonebook()
                view.print_message(f"Контакт '{contact.name}' добавлен.")
        elif choice == "3":
            if not phonebook or not len(phonebook["contacts"]):
                view.print_message("Справочник пуст.")
            else:
                view.find_contact_menu()
                find_choice = view.input_data("Выберите параметр поиска (1–5): ")

                if find_choice in ["1","2","3","4"]:
                    contact_list = list_contacts_found(phonebook,find_choice)

                    if not contact_list or not len(contact_list):
                        view.print_message("\nКонтакт не найден!")
                    else:
                        if len(contact_list) > 1:
                            deleted_contact = select_contact(contact_list, 'Выберите контакт для удаления')
                        else:
                            deleted_contact = contact_list[0]

                        if len(deleted_contact) > 0:
                            data = model.delete_contact(phonebook, deleted_contact.get("id"))
                            writer = model.SaveData(phonebook_path.file_path, data)
                            writer.save_phonebook()
                            view.print_message(f"Контакт '{deleted_contact.get("name")}' удалён.")

        elif choice == "4":
            if not phonebook or not len(phonebook["contacts"]):
                view.print_message("Справочник пуст.")
            else:
                view.find_contact_menu()
                find_choice = view.input_data("Выберите параметр поиска (1–5): ")

                if find_choice in ["1","2","3","4"]:
                    contact_list = list_contacts_found(phonebook, find_choice)

                    if not contact_list or not len(contact_list):
                        view.print_message("\nКонтакт не найден!")
                    else:
                        if len(contact_list) > 1:
                            edited_contact = select_contact(contact_list, 'Выберите контакт для изменения')
                        else:
                            edited_contact = contact_list[0]

                        if len(edited_contact) > 0:
                            view.edit_contact_menu()
                            edit_choice = view.input_data("Выберите данные для редактирования (1–3): ")

                            if edit_choice in ["1","2","3"]:
                                new_value = view.input_data("Введите новое значение: ")
                                data = model.edit_contact(phonebook, edited_contact.get("id"), edit_choice, new_value)
                                writer = model.SaveData(phonebook_path.file_path, data)
                                writer.save_phonebook()
                                view.print_message(f"Контакт '{edited_contact.get("name")}' изменён.")

        elif choice == "5":
            if not phonebook or not len(phonebook["contacts"]):
                view.print_message("Справочник пуст.")
            else:
                view.find_contact_menu()
                find_choice = view.input_data("Выберите параметр поиска (1–5): ")

                if find_choice in ["1", "2", "3", "4"]:
                    contact_list = list_contacts_found(phonebook, find_choice)

                    if not contact_list or not len(contact_list):
                        view.print_message("\nКонтакт не найден!")
                    else:
                        view.print_contact(contact_list)

        elif choice == "6":
            view.print_message("До свидания!")
            break
        else:
            view.print_message("Неверный выбор. Пожалуйста, введите число от 1 до 6.")

        view.show_main_menu()
        choice = view.input_data("Выберите действие (1–6): ")