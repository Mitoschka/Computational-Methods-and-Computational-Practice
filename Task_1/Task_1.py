import math
import sys
import os
from colorama import init, Fore

separations = []


def print_conditions(a: float, b: float, n: float, eps: float):
    print()
    print(Fore.GREEN + "Задание №1. ЧИСЛЕННЫЕ МЕТОДЫ РЕШЕНИЯ НЕЛИНЕЙНЫХ УРАВНЕНИЙ. Вариант 13")
    print(Fore.GREEN + "Исходные па-раметры задачи:")
    print("A =", a)
    print("B =", b)
    print("N =", n)
    print("f(x) = sin(x) + x^3 - 9 * x + 3")
    print("ε =", eps)


def root_separation(a: float, b: float, n: float):
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
            print(Fore.CYAN + f"Функция имеет {count} корня(-ей) на данном отрезке", end="\n\n")
            for separation in separations:
                print(f"[{separation[0]}, {separation[1]}]")
            is_end = True


def bisection(a: float, b: float, eps: float, separation):
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
            print(Fore.GREEN + "Метод Бисекции")
            print(f"Отрезок: [{separation[0]}, {separation[1]}]")
            print(f"Начальное приближение = {a}")
            print(f"Приблизительный корень = {X}")
            print(f"Модуль невязки = {math.fabs(f(X))}")
            print(f"Длина последнего отрезка = {Δ}")
            print(f"Число шагов: {count}")
            is_end = True


def newton_method(a: float, b: float, eps: float, separation):
    Δ = 0
    p = 1
    count = 0
    x_1 = (a + b) / 2
    x_2 = x_1 - (f(x_1) / df(x_1))
    while math.fabs(x_1 - x_2) > eps:
        if df(x_1) != 0:
            x_1 = x_2
            x_2 = x_1 - p * (f(x_1) / df(x_1))
            count += 1
        else:
            count = 1
            p += 2
            x_1 = (a + b) / 2
            x_2 = x_1 - p * (f(x_1) / df(x_1))
    Δ = math.fabs(x_1 - x_2)
    print(Fore.GREEN + "Метод Ньютона")
    print(f"Отрезок: [{separation[0]}, {separation[1]}]")
    print(f"Начальное приближение = {a}")
    print(f"Приблизительный корень = {x_2}")
    print(f"Модуль невязки = {math.fabs(f(x_2))}")
    print(f"Длина последнего отрезка = {Δ}")
    print(f"Число шагов: {count}")


def newton_mod_method(a: float, b: float, eps: float, separation):
    count = 0
    x_0 = (a + b) / 2
    x_1 = b
    x_2 = x_0

    while math.fabs(x_2 - x_1) > eps:
        x_1 = x_2
        x_2 = x_1 - f(x_1) / df(x_0)
        count += 1

    x = (x_1 + x_2) / 2

    Δ = (math.fabs(x_2 - x_1)) / 2
    print(Fore.GREEN + "Модифицированный метод Ньютона")
    print(f"Отрезок: [{separation[0]}, {separation[1]}]")
    print(f"Начальное приближение = {a}")
    print(f"Приблизительный корень = {x}")
    print(f"Модуль невязки = {math.fabs(f(x))}")
    print(f"Длина последнего отрезка = {Δ}")
    print(f"Число шагов: {count}")


def secant(a: float, b: float, eps: float, separation):
    count = 2
    x_0 = a
    x_1 = b
    x_2 = x_1 - (f(x_1) / df(x_0))
    Δ = 0

    while math.fabs(x_1 - x_2) > eps:
        x_0 = x_1
        x_1 = x_2
        x_2 = x_1 - f(x_1) * (x_1 - x_0) / (f(x_1) - f(x_0))
        count += 1

    Δ = (math.fabs(x_1 - x_2)) / 2
    print(Fore.GREEN + "Метод секущих")
    print(f"Отрезок: [{separation[0]}, {separation[1]}]")
    print(f"Начальное приближение = {a}, {b}")
    print(f"Приблизительный корень = {x_2}")
    print(f"Модуль невязки = {math.fabs(f(x_2))}")
    print(f"Длина последнего отрезка = {Δ}")
    print(f"Число шагов: {count}")


def f(x: float):
    return math.sin(x) + x ** 3 - 9 * x + 3


def df(x: float):
    return 3 * x ** 2 + math.cos(x) - 9
    

def print_menu():
    print()
    print(Fore.CYAN + "Меню действий:", end="\n\n")
    print("0 - Вывести исходные данные и параметры задачи")
    print("1 - Изменить исходные данные и параметры задачи")
    print("2 - Применить процедуру отделения корней")
    print("3 - Применить метод половинного деления (метод бисекции)")
    print("4 - Применить метод Ньютона (метод касательных)")
    print("5 - Применить модифицированный метод Ньютона")
    print("6 - Применить метод секущих")
    print("7 - Очистить консоль")
    print("8 - Завершить работу")


def main():
    init(autoreset = True)
    a = -5.0
    b = 4.0
    n = 10.0
    eps = 1e-8
    isExit = False
    root_is_separation = False

    print_menu()
    while not isExit:
        print()
        print(
            "---------------------------------------------------------------------------------------------"
        )
        print()
        print(Fore.BLUE + "Выполнить команду (Вызов меню - 9): ", end="")
        commad_number = int(input())

        if commad_number == 0:
            print_conditions(a, b, n, eps)
        elif commad_number == 1:
            print("Введите значение А: ", end="")
            a = float(input())
            print("Введите значение B: ", end="")
            b = float(input())
            print("Введите значение N: ", end="")
            n = float(input())
            print("Введите значение ε: ", end="")
            eps = float(input())
            root_is_separation = False
        elif commad_number == 2:
            root_separation(a, b, n)
            root_is_separation = True
        elif commad_number == 7:
            os.system("cls" if os.name == "nt" else "clear")
        elif commad_number == 8:
            sys.exit()
        elif commad_number == 9:
            print_menu()
        elif not root_is_separation and 0 <= commad_number <= 8 :
            print()
            print(Fore.RED + "Примените процедуру отделения корней")
        elif commad_number == 3:
            count = 1
            for separation in separations:
                print()
                print(Fore.CYAN + f"Результат выполнения для {count} отрезка", end="\n\n")
                a = separation[0]
                b = separation[1]
                bisection(a, b, eps, separation)
                count += 1
        elif commad_number == 4:
            count = 1
            for separation in separations:
                print()
                print(Fore.CYAN + f"\nРезультат выполнения для {count} отрезка", end="\n\n")
                a = separation[0]
                b = separation[1]
                newton_method(a, b, eps, separation)
                count += 1
        elif commad_number == 5:
            count = 1
            for separation in separations:
                print()
                print(Fore.CYAN + f"\nРезультат выполнения для {count} отрезка", end="\n\n")
                a = separation[0]
                b = separation[1]
                newton_mod_method(a, b, eps, separation)
                count += 1
        elif commad_number == 6:
            count = 1
            for separation in separations:
                print()
                print(Fore.CYAN + f"\nРезультат выполнения для {count} отрезка", end="\n\n")
                a = separation[0]
                b = separation[1]
                secant(a, b, eps, separation)
                count += 1
        else:
            print()
            print(Fore.RED + "Я не знаю такой команды :(")


main()
