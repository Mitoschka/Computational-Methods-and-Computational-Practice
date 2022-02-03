import sys
import os
import math
import scipy.integrate as integrate
from colorama import init, Fore
from tabulate import tabulate

# Полиномы степени 13, 11, 9, 7 и их интегралы
def polynomial_13(x):
    return 52 * (x ** 13) - 32 * (x ** 6) + (x ** 4) - 4


def I_13(x):
    return ((26 * x ** 14) / 7) - ((32 * x ** 7) / 7) + (x ** 5 / 5) - 4 * x


def polynomial_11(x):
    return 48 * (x ** 11) - 30 * (x ** 5) + (x ** 3) - 3


def I_11(x):
    return (4 * x ** 12) - (5 * x ** 6) + (x ** 4 / 4) - (3 * x)


def polynomial_9(x):
    return 42 * (x ** 9) - 24 * (x ** 5) + x - 2


def I_9(x):
    return ((21 * x ** 10) / 5) - (4 * x ** 6) + (x ** 2 / 2) - 2 * x


def polynomial_7(x):
    return 40 * (x ** 7) - 24 * (x ** 5) - 1


def I_7(x):
    return (5 * x ** 8) - (4 * x ** 6) - x


def check_polynomial(polynomial, i_polynomial, nodes, coefficients):
    j = i_polynomial(1) - i_polynomial(-1)
    j_g = sum([polynomial(pair[0]) * pair[1] for pair in zip(nodes, coefficients)])

    print(f"I точн. = {j}")
    print(f"I прибл. = {j_g}")
    print(f"|I точн. - I прибл.| = {math.fabs(j - j_g)}", end="\n\n")


# Функция f(x) для КФ Гаусса
def f_g(x):
    return math.sqrt(x) * math.exp(x ** 2)


# Интеграл функции f(x) для КФ Гаусса на [a, b]
def integrate_f_g(a, b):
    I_g, _ = integrate.quad(lambda x: f_g(x), a, b)
    return I_g


# Функция f(x) для КФ Мелера
def f_m(x):
    return (math.log(2 + x)) / (1 + x ** 3)


# Интеграл произведения функции f(x) на p(x) для КФ Мелера на [-1, 1]
def integrate_f_m():
    I_m, _ = integrate.quad(lambda x: f_m(x) / (math.sqrt(1 - x ** 2)), -1, 1)
    return I_m


# Многочлен Лежандра
def lejandre_polynomial(x, n):
    if n == 0:
        return 1
    elif n == 1:
        return x
    else:
        return ((2 * n - 1) / n) * lejandre_polynomial(x, n - 1) * x - (((n - 1) / n) * lejandre_polynomial(x, n - 2))


# Коэффициенты КФ Гаусса
def get_coefficients(nodes, n):
    coefficients = []

    for node in nodes:
        coefficient = (2 * (1 - (node ** 2))) / ((n ** 2) * (lejandre_polynomial(node, n - 1) ** 2))
        coefficients.append(coefficient)

    return coefficients


# Метод секущих
def secant_method(left_border, right_border, n, eps=1e-13):
    nodes = []
    h = (right_border - left_border) / (2 * n + (n % 2) + 2)

    # Секущая
    for i in range(0, 2 * n + (n % 2) + 2):
        x0 = left_border + i * h
        x1 = left_border + (i + 1) * h

        # Сохраняем начальные значения
        fx0 = lejandre_polynomial(x0, n)
        fx1 = lejandre_polynomial(x1, n)

        if fx0 * fx1 < 0:
            while abs(fx1) > eps:
                # Выполняем расчёт
                x2 = (x0 * fx1 - x1 * fx0) / (fx1 - fx0)
                # Сдвиг переменных (подготовка к следующему циклу)
                x0, x1 = x1, x2
                fx0, fx1 = fx1, lejandre_polynomial(x2, n)

            nodes.append(x1)

    return nodes


# Узлы и коэффициенты подобной КФ
def similar_quadrature_formula(a, b, nodes, coefficients):
    n_nodes = nodes.copy()
    n_coefficients = coefficients.copy()

    for i in range(0, len(n_nodes)):
        n_nodes[i] = 0.5 * (a + b + (b - a) * n_nodes[i])

    for i in range(0, len(n_coefficients)):
        n_coefficients[i] = ((b - a) / 2) * n_coefficients[i]

    J = sum([f_g(n_nodes[i]) * n_coefficients[i] for i in range(0, len(n_nodes))])

    return n_nodes, n_coefficients, J


# Печать узлов и коэффициентов
def print_table(nodes, coefficients, n):

    headers = ["№", "Узел", "Коэффицент"]
    counter = []
    nodes_list = []
    coefficients_list = []

    col_width = max([len(str(node)) for node in nodes])

    for i in range(0, n):
        counter.append(i + 1)
        nodes_list.append(str(nodes[i]).ljust(col_width))
        coefficients_list.append(coefficients[i])

    table = zip(counter, nodes_list, coefficients_list)

    print("\n" + tabulate(table, headers, floatfmt=".20e", tablefmt="grid"))


def definition_of_nodes_and_coefficients():
    print(Fore.GREEN + "\nОпределение узлов и коэффициентов:")
    all_nodes = []
    all_coefficients = []

    for i in range(1, 13):
        nodes = secant_method(-1, 1, i)
        coefficients = get_coefficients(nodes, i)

        all_nodes.append(nodes)
        all_coefficients.append(coefficients)

        print(Fore.CYAN + f"\nn = {i}:")
        print_table(nodes, coefficients, i)
        print("\nChecksum:", sum(coefficients), "\n")

    return all_nodes, all_coefficients


def print_conditions(a, b):
    print()
    print(Fore.GREEN + "Задание №5. Вариант #13")
    print(Fore.GREEN + "КФ Гаусса, ее узлы и коэффициенты. Вычисление интегралов при помощи КФ Гаусса")
    print(Fore.GREEN + "КФ Мелера, ее узлы и коэффициенты. Вычисление интегралов при помощи КФ Мелера")
    print()
    print(Fore.CYAN + "Исходные данные и параметры задачи:")
    print(f"a = {a}")
    print(f"b = {b}")
    print("f(x) = sqrt(x) * exp(x ^ 2) для КФ Гаусса")
    print("f(x) = (ln(2 + x)) / (1 + x ^ 3) для КФ Мелера")


def print_menu():
    print()
    print(Fore.CYAN + "Меню действий:", end="\n\n")
    print("0 - Вывести исходные данные и параметры задачи")
    print("1 - Изменить исходные данные и параметры задачи")
    print("2 - Определить узлы и коэффициенты")
    print("3 - Осуществить проверку точности на многочлене наивысшей степени")
    print("4 - Вычисление при помощи КФ Гаусса")
    print("5 - Вычисление при помощи КФ Мелера")
    print("6 - Очистить консоль")
    print("7 - Завершить работу")


def main():
    init(autoreset=True)

    a = 0
    b = 1
    isExit = False

    all_nodes, all_coefficients = definition_of_nodes_and_coefficients()
    print_menu()
    print()
    while not isExit:
        print()
        print("-" * 120)
        print()
        print(Fore.BLUE + "Выполнить команду (Вызов меню - 8): ", end="")
        try:
            commad_number = int(input())
        except:
            commad_number = 9

        if commad_number == 0:
            print_conditions(a, b)

        elif commad_number == 1:
            try:
                a = float(input("Введите значение левой границы интегрирования (a): "))
            except:
                a = float(0)
            try:
                b = float(input("Введите значение правой границы интегрирования (b): "))
            except:
                b = float(1)

            if a > b:
                a, b = b, a

        elif commad_number == 2:
            all_nodes, all_coefficients = definition_of_nodes_and_coefficients()

        elif commad_number == 3:
            # Проверка точности на на многочленах наивысших степеней
            print(Fore.GREEN + "\nВыборочная проверка точности\n\n")
            print(Fore.CYAN + "Полином 13 степени:\n")
            check_polynomial(polynomial_13, I_13, all_nodes[7], all_coefficients[7])
            print(Fore.CYAN + "Полином 11 степени:\n")
            check_polynomial(polynomial_11, I_11, all_nodes[6], all_coefficients[6])
            print(Fore.CYAN + "Полином 9 степени:\n")
            check_polynomial(polynomial_9, I_9, all_nodes[5], all_coefficients[5])
            print(Fore.CYAN + "Полином 7 степени:\n")
            check_polynomial(polynomial_7, I_7, all_nodes[4], all_coefficients[4])

        elif commad_number == 4:
            # Вычисление интеграла из задания варианта #13
            print(Fore.GREEN + "\nВычисление интеграла из задания варианта #13")
            print(Fore.GREEN + f"sqrt(x) * e^x^2 на [{a}, {b}], N = 4, 5, 6, 7")

            for count in [9, 10, 11, 12]:
                n_nodes, n_coefficients, J = similar_quadrature_formula(
                    a, b, all_nodes[count - 1], all_coefficients[count - 1]
                )
                print(Fore.CYAN + f"\nПри N = {count}:\n")
                print_table(n_nodes, n_coefficients, count)
                print(f"\nI прибл. = {J}")
                print(f"I точн. = {integrate_f_g(a, b)}")
                print(f"|I точн. - I прибл.| = {math.fabs(integrate_f_g(a, b) - J)}", end="\n")
                print("\nChecksum:", sum(n_coefficients), "\n\n")

        elif commad_number == 5:
            # КФ Мелера
            print(Fore.GREEN + "\nПриближённое вычисление при помощи КФ Мелера")
            print(Fore.GREEN + "f(x) = ln(2+x) / (1 + x^3) \n")

            # Ввод n1, n2, n3
            try:
                n1 = int(input("Введите значения N1: "))
            except:
                n1 = int(1)
            try:
                n2 = int(input("Введите значения N2: "))
            except:
                n2 = int(2)
            try:
                n3 = int(input("Введите значения N3: "))
            except:
                n3 = int(3)

            for n in [n1, n2, n3]:
                m_nodes = [math.cos(math.pi * ((2 * i - 1) / (2 * n))) for i in range(1, n + 1)]
                J = (math.pi / n) * sum([f_m(node) for node in m_nodes])
                print(Fore.CYAN + f"\nПри N = {n}:\n")
                print_table(m_nodes, [math.pi / n for i in range(0, len(m_nodes))], len(m_nodes))
                print(f"\nI прибл. = {J}")
                print(f"I точн. = {integrate_f_m()}")
                print(f"|I точн. - I прибл.| = {math.fabs(integrate_f_m() - J)}", end="\n")
                print("\nChecksum:", sum([math.pi / n for i in range(0, len(m_nodes))]))

        elif commad_number == 6:
            os.system("cls" if os.name == "nt" else "clear")

        elif commad_number == 7:
            sys.exit()

        elif commad_number == 8:
            os.system("cls" if os.name == "nt" else "clear")
            print_menu()

        else:
            print(Fore.RED + "\nЯ не знаю такой команды :(")


if __name__ == "__main__":
    main()
