import sys
import os
import math
from colorama import init, Fore


def print_conditions(a, h, m):
    print()
    print(Fore.GREEN + "Задание №3.2. Вариант 13")
    print(Fore.GREEN + "Нахождение производных таблично-заданной функции")
    print(Fore.GREEN + "по формулам численного дифференцирования")
    print(Fore.GREEN + "Исходные па-раметры задачи:")
    print("a =", a)
    print("h =", h)
    print("m =", m)
    print("\nf(x) = exp^(6*x)")


def f(x):
    return math.exp(6 * x)


def f_first_derivative(x):
    return math.exp(6 * x) * 6


def f_second_derivative(x):
    return math.exp(6 * x) * 36


def column_of_x_i(a: int, h: float, m: int):
    list_of_x_i = []

    for i in range(m):
        x_i = a + i * h
        list_of_x_i.append((x_i))

    return list_of_x_i


def column_of_fx(a: int, h: float, m: int):
    list_of_fx = []

    for i in range(m):
        x_i = a + i * h
        list_of_fx.append(f(x_i))

    return list_of_fx


def search_first_derivative(fx, h):
    list_of_first_derivative = []
    list_of_first_derivative.append((-3 * fx[0] + 4 * fx[1] - fx[2]) / (2 * h))

    for i in range(1, len(fx) - 1):
        list_of_first_derivative.append((fx[i + 1] - fx[i - 1]) / (2 * h))

    list_of_first_derivative.append((3 * fx[len(fx) - 1] - 4 * fx[len(fx) - 2] + fx[len(fx) - 3]) / (2 * h))

    return list_of_first_derivative


def search_second_derivative(fx, h):
    list_of_second_derivative = []
    list_of_second_derivative.append(None)

    for i in range(1, len(fx) - 1):
        list_of_second_derivative.append((fx[i + 1] - 2 * fx[i] + fx[i - 1]) / (math.pow(h, 2)))

    list_of_second_derivative.append(None)

    return list_of_second_derivative


def print_table(x_i, fx, first_derivative, second_derivative):
    list_of_different_of_first_derivative = []
    list_of_different_of_second_derivative = []

    if len(x_i) == 0:
        for i in range(len(x_i)):
            list_of_different_of_first_derivative.append(abs(first_derivative[i] - f_first_derivative(x_i[i])))
    else:
        for i in range(len(x_i)):
            list_of_different_of_first_derivative.append(abs(first_derivative[i] - f_first_derivative(x_i[i])))
            if second_derivative[i] == None:
                list_of_different_of_second_derivative.append(None)
            else:
                list_of_different_of_second_derivative.append(abs(second_derivative[i] - f_second_derivative(x_i[i])))

    table = [x_i, fx, first_derivative, list_of_different_of_first_derivative, second_derivative, list_of_different_of_second_derivative]

    print("x", " " * 13,
        "f(x)", " " * 10,
        "f'(x)чд", " " * 3, 
        "|f'(x)т - f'(x)чд|", " ",
        "f''(x)чд", " ",
        "|f''(x)т - f''(x)чд|")
    for i in range(len(x_i)):
        print()
        print("{:e}".format(table[0][i]), end='\t')
        print("{:e}".format(table[1][i]), end='\t')
        print("{:e}".format(table[2][i]), end='\t')
        print("{:e}".format(table[3][i]), end='\t')
        try:
            print("{:e}".format(table[4][i]), end='\t')
        except:
            print(table[4][i], end="\t")
        try:
            print("{:e}".format(table[5][i]))
        except:
            print(" " * 7, table[5][i])



def print_menu():
    print()
    print(Fore.CYAN + "Меню действий:", end="\n\n")
    print("0 - Вывести исходные данные и параметры задачи")
    print("1 - Вывести таблицу")
    print("2 - Очистить консоль")
    print("3 - Завершить работу")


def main():
    init(autoreset=True)
    a = 1
    h = 10 ** (-6)
    m = 5
    isExit = False

    print_menu()
    while not isExit:
        print()
        print("-" * 120)
        print()
        print(Fore.BLUE + "Выполнить команду (Вызов меню - 4): ", end="")

        try:
            commad_number = int(input())
        except:
            commad_number = 5

        if commad_number == 0:
            print_conditions(a, h, m)
        elif commad_number == 1:
            try:
                print("Введите значение a:")
                a = float(input())
            except:
                a = 1
            try:
                print("Введите значение (h > 0):")
                h = float(input())
            except:
                h = 10 ** (-6)
            try:
                print("Введите значение (m + 1):")
                m = float(input())
            except:
                m = 5

            x_i = column_of_x_i(a, h, m)
            fx = column_of_fx(a, h, m)
            first_derivative = search_first_derivative(fx, h)
            second_derivative = search_second_derivative(fx, h)

            print_table(x_i, fx, first_derivative, second_derivative)
        elif commad_number == 2:
            os.system("cls" if os.name == "nt" else "clear")
        elif commad_number == 3:
            sys.exit()
        elif commad_number == 4:
            os.system("cls" if os.name == "nt" else "clear")
            print_menu()
        else:
            print(Fore.RED + "\nЯ не знаю такой команды :(")


if __name__ == "__main__":
    main()
