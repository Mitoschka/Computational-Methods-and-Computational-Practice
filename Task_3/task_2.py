import sys
import os
from colorama import init, Fore
from tabulate import tabulate


class Root:
    def __init__(self, arg, value):
        self.arg = arg
        self.value = value
        self.distance = None

    def set_distance(self, new_arg):
        self.distance = abs(self.arg - new_arg)


def print_conditions(a: float, b: float, n: float, m: int, x: float):
    print()
    print(Fore.GREEN + "Задание №2. Вариант 13")
    print(Fore.GREEN + "Задача алгебраического интерполирования.")
    print(Fore.GREEN + "Интерполяционный многочлен в форме Ньютона и в форме Лагранжа.")
    print(Fore.GREEN + "Исходные па-раметры задачи:")
    print("a =", a)
    print("b =", b)
    print("n =", n)
    print("m =", m)
    print("x =", x)
    print("f(x) = ln(1 + x) - exp(x)")
    print("x_j = a + j * (b - a) / m")
    print("j = 0,1...m")


def f(x: float):
    return -0.175 * x**4


def tabulate_value(a, b, m, func,  reversed = False):
    table = []
    for i in range(m + 1):
        arg = a + (b - a) * i / m
        if reversed:
            root = Root(func(arg), arg)
        else:
            root = Root(arg, func(arg))
        table.append(root)
    return table


def lagrange(table, x, n):
    res = 0
    # суммирование l_{kn} по k
    for k in range(n + 1):
        res_k = 1
        # умножение (x - x_i) / (x_k - x_i) по i
        for i in range(n + 1):
            if i != k:
                res_k *= (x - table[i].arg) / (table[k].arg - table[i].arg)
        res += res_k * table[k].value

    return res


def newton(table, x, n):
    res = 0

    diff_table = []

    for i in range(n + 1):
        diff_table.append([table[i].value])
    for j in range(n):
        for i in range(n - j):
            diff_value = (diff_table[i + 1][-1] - diff_table[i][-1]) / (
                table[i + j + 1].arg - table[i].arg
            )
            diff_table[i].append(diff_value)

    for k in range(n + 1):
        res_x_multiply = 1
        for j in range(k):
            res_x_multiply *= x - table[j].arg
        res += diff_table[0][k] * res_x_multiply

    print()
    print(Fore.GREEN + "Таблица разделенных разностей:")
    for list in diff_table:
        print()
        print("[ ", end="")
        for element in list:
            print("{:e}".format(element), end=" ")
        print("]", end="")
    print("\n")
    return res


def print_table(table, show_distance=False, reversed=False):
    element_of_table = []
    if show_distance:
        if reversed:
            headers_of_table = ["f(x)", "x", "distance"]
        else:
            headers_of_table = ["x", "f(x)", "distance"]
        for root in table:
            element_of_table.append(
                (
                    "{:e}".format(root.arg),
                    "{:e}".format(root.value),
                    "{:e}".format(root.distance),
                )
            )
        print(tabulate(element_of_table, headers_of_table, tablefmt="pretty"))
    else:
        if reversed:
            headers_of_table = ["f(x)", "x"]
        else:
            headers_of_table = ["x", "f(x)"]
        for root in table:
            element_of_table.append(
                ("{:e}".format(root.arg), "{:e}".format(root.value))
            )
        print(tabulate(element_of_table, headers_of_table, tablefmt="pretty"))


def solve_request(table, x_0: float):

    for root in table:
        root.set_distance(x_0)

    sorted_table = sorted(table, key=lambda o: o.distance)
    return sorted_table


def lagrange_res(sorted_table, x_0: float, n):
    lagrange_res = lagrange(sorted_table, x_0, n)
    print()
    print(Fore.GREEN + "Интерполяция Лагранжа:")
    print("P_{n}^{L}(x) =", "{:e}".format(lagrange_res))
    print("|f(x) - P_{n}^{L}(x)|= ", "{:e}".format(abs(lagrange_res - f(x_0))))


def newton_res(sorted_table, x_0: float, n):
    newton_res = newton(sorted_table, x_0, n)
    print()
    print(Fore.GREEN + "Интерполяция Ньютона:")
    print("P_{n}^{N}(x) =", "{:e}".format(newton_res))
    print("|f(x) - P_{n}^{N}(x)| =", "{:e}".format(abs(newton_res - f(x_0))))


def print_sub_menu_table():
    print()
    print(Fore.CYAN + "Меню действий:", end="\n\n")
    print("0 - Вывести таблицу значений функции")
    print("1 - Вывести отсортированную таблицу (набор узлов)")
    print("2 - Вывести оба варианта")
    print("3 - Вернуться назад")
    print("4 - Очистить консоль")
    print("5 - Завершить работу")


def print_sub_menu_result():
    print()
    print(Fore.CYAN + "Меню действий:", end="\n\n")
    print("0 - Вывести результат интерполяции (Лагранж)")
    print("1 - Вывести результат интерполяции (Ньютон)")
    print("2 - Вывести оба варианта")
    print("3 - Вернуться назад")
    print("4 - Очистить консоль")
    print("5 - Завершить работу")


def print_menu():
    print()
    print(Fore.CYAN + "Меню действий:", end="\n\n")
    print("0 - Вывести исходные данные и параметры задачи")
    print("1 - Изменить исходные данные и параметры задачи")
    print("2 - Вывести таблицу")
    print("3 - Вывести результаты")
    print("4 - Выполнить всё")
    print("5 - Очистить консоль")
    print("6 - Завершить работу")


def main():
    init(autoreset=True)
    a = 0
    b = 3
    n = 7
    m = 15
    x = 2
    isExit = False
    is_menu = True
    is_sub_menu_table = False
    is_sub_menu_result = False

    print_menu()
    while not isExit:
        print()
        print("-" * 120)
        print()
        print(Fore.BLUE + "Выполнить команду (Вызов меню - 7): ", end="")
        commad_number = int(input())

        if is_menu:
            print()
            if commad_number == 0:
                print_conditions(a, b, n, m, x)
            elif commad_number == 1:
                print("Введите значение a:")
                a = int(input())
                print("Введите значение b:")
                b = int(input())
                print("Введите число значений в таблице (m+1):")
                m = int(input())
                print(f"Введите степень многочлена n < {m}:")
                n = int(input())
                while n > m:
                    print(Fore.RED + "Введено недопустимое значение n!")
                    print(f"Введите степень многочлена n < {m}:")
                    n = int(input())
                print(f"Введите значение x:")
                x = float(input())
            elif commad_number == 2:
                os.system("cls" if os.name == "nt" else "clear")
                is_sub_menu_table = True
                is_menu = False
                print_sub_menu_table()
                continue
            elif commad_number == 3:
                os.system("cls" if os.name == "nt" else "clear")
                is_sub_menu_result = True
                is_menu = False
                print_sub_menu_result()
                continue
            elif commad_number == 4:
                table = tabulate_value(a, b, m - 1, f)
                print_table(table)
                sorted_table = solve_request(table, x)
                print(Fore.GREEN + "\nОтсортированная таблица:")
                print_table(sorted_table, show_distance=True)
                lagrange_res(sorted_table, x, n)
                newton_res(sorted_table, x, n)
            elif commad_number == 5:
                os.system("cls" if os.name == "nt" else "clear")
            elif commad_number == 6:
                sys.exit()
            elif commad_number == 7:
                os.system("cls" if os.name == "nt" else "clear")
                print_menu()
            else:
                print(Fore.RED + "Я не знаю такой команды :(")

        if is_sub_menu_table:
            print()
            if commad_number == 0:
                table = tabulate_value(a, b, m - 1, f)
                print_table(table)
            elif commad_number == 1:
                table = tabulate_value(a, b, m - 1, f)
                sorted_table = solve_request(table, x)
                print(Fore.GREEN + "\nОтсортированная таблица:")
                print_table(sorted_table, show_distance=True)
            elif commad_number == 2:
                table = tabulate_value(a, b, m - 1, f)
                print_table(table)
                sorted_table = solve_request(table, x)
                print(Fore.GREEN + "\nОтсортированная таблица:")
                print_table(sorted_table, show_distance=True)
            elif commad_number == 3:
                os.system("cls" if os.name == "nt" else "clear")
                is_sub_menu_table = False
                is_menu = True
                print_menu()
                continue
            elif commad_number == 4:
                os.system("cls" if os.name == "nt" else "clear")
            elif commad_number == 5:
                sys.exit()
            elif commad_number == 7:
                os.system("cls" if os.name == "nt" else "clear")
                print_sub_menu_table()
            else:
                print(Fore.RED + "Я не знаю такой команды :(")

        if is_sub_menu_result:
            print()
            if commad_number == 0:
                table = tabulate_value(a, b, m - 1, f)
                sorted_table = solve_request(table, x)
                lagrange_res(sorted_table, x, n)
            elif commad_number == 1:
                table = tabulate_value(a, b, m - 1, f)
                sorted_table = solve_request(table, x)
                newton_res(sorted_table, x, n)
            elif commad_number == 2:
                table = tabulate_value(a, b, m - 1, f)
                sorted_table = solve_request(table, x)
                lagrange_res(sorted_table, x, n)
                newton_res(sorted_table, x, n)
            elif commad_number == 3:
                os.system("cls" if os.name == "nt" else "clear")
                is_sub_menu_result = False
                is_menu = True
                print_menu()
                continue
            elif commad_number == 4:
                os.system("cls" if os.name == "nt" else "clear")
            elif commad_number == 5:
                sys.exit()
            elif commad_number == 7:
                os.system("cls" if os.name == "nt" else "clear")
                print_sub_menu_result()
            else:
                print(Fore.RED + "Я не знаю такой команды :(")