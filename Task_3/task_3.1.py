import sys
import os
import math
from colorama import init, Fore
from tabulate import tabulate


def print_conditions(a: float, b: float, m: float, exp: float):
    print()
    print(Fore.GREEN + "Задание №3.1. Вариант 13")
    print(Fore.GREEN + "Задача обратного алгебраического интерполирования.")
    print(Fore.GREEN + "Исходные па-раметры задачи:")
    print("a =", a)
    print("b =", b)
    print("m =", m)
    print("exp =", "{:e}".format(exp))
    print("f(x) = ln(1 + x) - exp(x)")


def create_table(a: float, b: float, m: int):
    column_of_x_i = []
    column_of_f_x = []
    element_of_table = []

    h = (b - a) / m
    for i in range(m + 1):
        x_i = a + i * h
        column_of_x_i.append(x_i)
        column_of_f_x.append(f(x_i))
        element_of_table.append((column_of_x_i[-1], column_of_f_x[-1]))

    return element_of_table


def print_table(table: list):
    headers_of_table = ["x", "f(x)"]
    print("\n" + tabulate(table, headers_of_table, floatfmt=".6e", tablefmt="psql"))


def input_of_current(m: int):
    try:
        print("Введите значение F (по умолчанию F = -5):")
        F = float(input())
    except:
        F = 0.3
    print(f"Введите степень многочлена n < {m}:")
    try:
        n = int(input())
        while n > m:
            print(Fore.RED + "Введено недопустимое значение n!")
            print(f"Введите степень многочлена n < {m}:")
            n = float(input())
    except: 
        n = 9

    return F, n


def f(x):
    return (x**2) / (1+x**2)


def reverse_table(table: list):
    swap_table = []
    for i in range(len(table)):
        swap_table.append((table[i][1], table[i][0]))

    return swap_table


def lagrange(table: list, F: float, n: int):
    res = 0
    for k in range(n + 1):
        res_k = 1
        for i in range(n + 1):
            if i != k:
                res_k *= (F - table[i][0]) / (table[k][0] - table[i][0])
                
        res += res_k * table[k][1]

    return res


def first_solution(table: list, F: float, n: int):
    sorted_table = table_sorting(table, F)
    swap_table = reverse_table(sorted_table)
    Qn_F = lagrange(swap_table, F, n)

    print(Fore.GREEN + f"\nQn_F = {Qn_F}")
    print(Fore.GREEN + f"Модуль невязки rn(X) = {math.fabs(f(Qn_F) - F)}")


def table_sorting(table: list, F: float):
    sorted_table = sorted(table, key=lambda y: math.fabs(y[1] - F))

    return sorted_table


def equation(table: list, x: float, F: float, n: int):
    return lagrange(table, x, n) - F


def root_separation(a: float, b: float, n: int, f):
    separations = []

    h = (b - a) / n
    count = 0
    x_1 = a
    x_2 = x_1 + h
    y_1 = f(x_1)
    is_end = False

    while is_end is False:
        if x_2 <= b:
            y_2 = f(x_2)
            if y_1 * y_2 <= 0:
                count += 1
                separation = [float(x_1), float(x_2)]
                separations.append(separation)
            x_1 = x_2
            x_2 = x_1 + h
            y_1 = y_2
        else:
            print()
            print(
                Fore.CYAN + f"Функция имеет {count} корня(-ей) на данном отрезке",
                end="\n\n",
            )
            for separation in separations:
                print(f"[{separation[0]}, {separation[1]}]")
            is_end = True

    return separations


def bisection(a: float, b: float, eps: float, f):
    is_end = False
    count = 0

    while is_end is False:
        c = (a + b) / 2
        if f(a) * f(c) <= 0:
            b = c
        else:
            a = c
        count += 1
        if not b - a > 2 * eps:
            X = (a + b) / 2
            Δ = (b - a) / 2
            print(Fore.GREEN + "\nМетод Бисекции")
            print(f"Отрезок: [{a}, {b}]")
            print(f"Начальное приближение = {a}")
            print(f"Приблизительный корень = {X}")
            print(f"Модуль невязки = {math.fabs(f(X))}")
            print(f"Длина последнего отрезка = {Δ}")
            print(f"Число шагов: {count}")
            is_end = True


def second_solution(table: list, a: float, b: float, F: float, n: int, exp: float):
    sorted_table = table_sorting(table, F)
    separations = root_separation(a, b, 999, lambda x: equation(sorted_table, x, F, n))
    for left, right in separations:
        bisection(left, right, exp, lambda x: equation(sorted_table, x, F, n))


def print_menu():
    print()
    print(Fore.CYAN + "Меню действий:", end="\n\n")
    print("0 - Вывести исходные данные и параметры задачи")
    print("1 - Изменить исходные данные и параметры задачи")
    print("2 - Вывести таблицу")
    print("3 - Решить первым способом (Qn(F))", Fore.RED + "Не применим для нестрого монотонной функции!")
    print("4 - Решить вторым способом (Pn(x))")
    print("5 - Очистить консоль")
    print("6 - Завершить работу")


def main():
    init(autoreset=True)
    a = 0
    b = 1
    m = 20
    exp = 10 ** (-8)
    isExit = False

    print_menu()
    while not isExit:
        print()
        print("-" * 120)
        print()
        print(Fore.BLUE + "Выполнить команду (Вызов меню - 7): ", end="")
        try:
            commad_number = int(input())
        except:
            commad_number = 8

        if commad_number == 0:
            print_conditions(a, b, m, exp)
        elif commad_number == 1:
            try:
                print("Введите значение a:")
                a = float(input())
            except:
                a = 0
            try:
                print("Введите значение b:")
                b = float(input())
            except:
                b = 1
            try:
                print("Введите значение (m + 1):")
                m = int(input())
            except:
                m = 9
            try:
                print("Введите значение exp:")
                exp = float(input())
            except:
                exp = 10 ** (-8)
        elif commad_number == 2:
            table = create_table(a, b, m)
            print_table(table)
        elif commad_number == 3:
            table = create_table(a, b, m)
            F, n = input_of_current(m)
            print_table(table)
            first_solution(table, F, n)
        elif commad_number == 4:
            table = create_table(a, b, m)
            F, n = input_of_current(m)
            print_table(table)
            second_solution(table, a, b, F, n, exp)
        elif commad_number == 5:
            os.system("cls" if os.name == "nt" else "clear")
        elif commad_number == 6:
            sys.exit()
        elif commad_number == 7:
            os.system("cls" if os.name == "nt" else "clear")
            print_menu()
        else:
            print(Fore.RED + "\nЯ не знаю такой команды :(")


if __name__ == '__main__':
    main()
