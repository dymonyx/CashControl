import json
import datetime

temp_array = []
actions = ["Добавить продукт", "Просмотреть все записи", "Просмотреть покупки по дате или категории",
           "Отсортировать данные по цене", "Удалить запись", "Выйти из программы"]
sorts = ["Сортировка от минимальной стоимости к максимальной", "Сортировка от максимальной стоимости к минимальной"]


def create_collection_template():
    return {
        "Дата": "",
        "Категория": "",
        "Название продукта": "",
        "Стоимость": ""
    }


def add_product(new_product):  # Добавление нового продукта
    main_data.append(new_product)
    file.seek(0)  # перемещение указателя в начало
    json.dump(main_data, file, ensure_ascii=False)
    file.truncate()  # обрезка всего, что идёт после новой добавленной информации


def create_product_dictionary(date, category, name, price):  # Создание словаря с новым продуктом
    new_product = create_collection_template()
    new_product["Дата"] = date
    new_product["Категория"] = category[0].upper() + category[1:].lower()
    new_product["Название продукта"] = name[0].upper() + name[1:].lower()
    new_product["Стоимость"] = price
    return new_product


def get_lengths(  # считаем длины заголовков для красивого вывода в косноль
        headers, new_array):
    len_first_header, len_second_header, len_third_header, len_fourth_header = map(len, headers[:])
    for i in range(len(new_array)):
        array = [j for j in new_array[i].values()]
        new_len_first_header, new_len_second_header, new_len_third_header, new_len_fourth_header = map(len, array[:])
        len_first_header, len_second_header, len_third_header, len_fourth_header = max(len_first_header,
                                                                                       new_len_first_header), max(
            len_second_header, new_len_second_header), max(len_third_header, new_len_third_header), max(
            len_fourth_header, new_len_fourth_header)
    lengths = [len_first_header, len_second_header, len_third_header, len_fourth_header,
               max(len(str(len(new_array))), len("Номер записи"))]
    return lengths


def output_function(headers, lengths, array):  # выводим красивые заголовки и инфу о продуктах
    print()
    # Вывод заголовков
    print("{:<{}} {:<{}} {:<{}} {:<{}} {:<{}}".format("Номер записи", lengths[4] + 5, headers[0], lengths[0] + 5,
                                                      headers[1], lengths[1] + 5,
                                                      headers[2], lengths[2] + 5,
                                                      headers[3],
                                                      lengths[3] + 5))
    print("=" * sum([lengths[4], lengths[0], lengths[1], lengths[2], lengths[3], 6 * (len(headers) + 1)]))

    # Вывод информации о продуктах
    for i in range(len(array)):
        information = [j for j in array[i].values()]
        print("{:<{}} {:<{}} {:<{}} {:<{}} {:<{}}".format(i + 1, lengths[4] + 5,
                                                          information[0], lengths[0] + 5, information[1],
                                                          lengths[1] + 5,
                                                          information[2],
                                                          lengths[2] + 5,
                                                          information[3],
                                                          lengths[3] + 5))

    print("=" * sum([lengths[4], lengths[0], lengths[1], lengths[2], lengths[3], 6 * (len(headers) + 1)]))
    print()


def display_products(array):  # вывод информации о продуктах
    headers = [i for i in array[0].keys()]
    lengths = get_lengths(headers, array)
    output_function(headers, lengths, array)
    global temp_array
    temp_array = array


def output_parameteres(output_parameter):  # извлекаем список запрашиваемых параметров
    print()
    output_parameter = output_parameter[0].upper() + output_parameter[1:].lower()
    parameters = list(set([i[output_parameter] for i in main_data]))
    if output_parameter == "Дата":
        parameters = sorted(list(parameters), key=lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'))
    for num, parameter in enumerate(parameters):
        print("{:<{}} {:<{}}".format("●", 3, parameter, len(max(parameters, key=len)) + 5))
    print()
    return parameters


def get_array(output_parameter, name_parameter):  # извлекаем список продуктов, подходящих под запрашиваемый параметр
    output_parameter = output_parameter[0].upper() + output_parameter[1:].lower()
    name_parameter = name_parameter[0].upper() + name_parameter[1:].lower()
    new_array = []
    for product in main_data:
        if product[output_parameter] == name_parameter:
            new_array.append(product)
    return new_array


def sorting(array, parameter):  # сортировка
    parameter = False if parameter == 1 else True
    global temp_array
    new_array = sorted(array, key=lambda x: float(list(x.values())[3]), reverse=parameter)
    temp_array = new_array
    return new_array


def delete_product(number):  # удаление продукта
    deleting_product = temp_array[number - 1]
    main_data.remove(deleting_product)
    file.seek(0)  # перемещение указателя в начало
    json.dump(main_data, file, ensure_ascii=False)
    file.truncate()  # обрезка всего, что идёт после новой добавленной информации


def output_actions(array):  # вывод списка доступных действий в консоль
    print()
    for num, name_action in enumerate(array):
        print("{:<{}} {:<{}}".format(num + 1, 1 + 5, name_action, len(max(array, key=len)) + 5))
    print()


def read_file():  # чтение файла
    global file
    global main_data
    file = open("main.json", "r+", encoding="utf-8")
    main_data = json.load(file)


def start_error_processing():  # обработка выбора действий
    output_actions(actions)
    while True:
        action = input("Введите номер действия: ")
        print()
        try:
            action = int(action)
        except ValueError:
            print("Вы ввели не число. Введите, пожалуйста, число от 1 до 6")
            output_actions(actions)
        else:
            if 1 <= action <= 6:
                return action
            else:
                print("Введённое число должно быть в диапазоне от 1 до 6")
                print()


def check_date(date):  # проверка даты на корректность
    try:
        date = datetime.datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        print()
        print("Введённая дата не соответствует формату.")
        return False
    else:
        today = datetime.datetime.today()
        if date <= today:
            return True
        else:
            print()
            print("Вы ввели дату из будущего.")
            return False


def isNumber(numb):  # проверка аргумента на то, является ли он числом
    try:
        float(numb)
    except ValueError:
        return False
    else:
        return True


def check_price(price):  # проверка цены на корректность
    if isNumber(price):
        if 0 < float(price) <= 10_000_000:
            return True
        else:
            print()
            print("Цена должна быть в диапазоне от 0 до 10_000_000.")
            return False
    else:
        print()
        print("Цена должна быть числом.")
        return False


def action_1():  # первое действие - добавление продукта, обработка ошибок
    date = input("Введите дату в формате День-Месяц-Год: ")
    if not check_date(date):
        print()
        print("Ошибка. Продукт не добавлен.")
        return 0
    category = input("Введите категорию: ")
    name = input("Введите название продукта: ")
    price = input("Введите цену: ")
    if not check_price(price):
        print()
        print("Ошибка. Продукт не добавлен.")
        return 0
    add_product(create_product_dictionary(date, category, name, price))
    print()
    print("Продукт успешно добавлен.")


def check_name_parameter(name_parameter, parameteres):  # проверка на нахождение введённого параметра в списке доступных
    if name_parameter[0].upper() + name_parameter[1:].lower() in parameteres:
        return True
    else:
        print("Введённая характеристика отсутствует в списке доступных.")
        return False


def is_int_Number(numb):  # проверка аргумента на целочисленность
    try:
        int(numb)
    except ValueError:
        return False
    else:
        return True


def action_3():
    output_parameter = input("Введите характеристику вывода (Дата, Категория): ")
    if output_parameter.lower() not in ["дата", "категория"]:
        print()
        print("Вы ввели неверную характеристику вывода. Доступные характеристики: Дата, Категория")
    else:
        parameteres = output_parameteres(output_parameter)
        name_parameter = input("Введите название характеристики: ")
        print()
        if check_name_parameter(name_parameter, parameteres):
            display_products(get_array(output_parameter, name_parameter))


def action_4():
    print("Какая сортировка вам нужна?: ")
    output_actions(sorts)
    parameter = input("Введите номер сортировки (1, 2) : ")
    if is_int_Number(parameter):
        if int(parameter) in [1, 2]:
            display_products(sorting(main_data, int(parameter)))
        else:
            print()
            print("Вы ввели неверный номер сортировки. Диапазон доступных сортировок: 1, 2")
    else:
        print()
        print("Вы ввели не целое число.")


def action_5():
    number = input("Введите номер записи, которую хотите удалить: ")
    if is_int_Number(number):
        if len(temp_array) == 0:
            print()
            print("Сначала выберите любое действие, с помощью которого можно просмотреть список продуктов. ")
        elif len(temp_array) == 1:
            if int(number) == 1:
                delete_product(int(number))
                print()
                print("Запись удалена успешно.")
            else:
                print()
                print("Вы ввели неверный номер записи. Диапазон доступных записей: 1")
        else:
            if 1 <= int(number) <= len(temp_array):
                delete_product(int(number))
                print()
                print("Запись удалена успешно.")
            else:
                print()
                print(f"Вы ввели неверный номер записи. Диапазон доступных записей: 1 - {len(temp_array)}")
    else:
        print()
        print("Вы ввели не целое число.")


def main_function():  # основная функция - вызывающая соответствующие функции для выполнения выбранных действий
    read_file()
    action = start_error_processing()
    while action != 6:
        if action == 1:
            action_1()
        elif action == 2:
            display_products(main_data)
        elif action == 3:
            action_3()
        elif action == 4:
            action_4()
        elif action == 5:
            action_5()
        action = start_error_processing()
    file.close()


if __name__ == "__main__":
    main_function()
