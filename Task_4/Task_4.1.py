import sys
import os
import math
import scipy.integrate as integrate
from colorama import init, Fore
from tabulate import tabulate


# АСТ 0 (алгебраическая степень точности)
def quadrature_formula_of_left_rect(f, a: float, b: float):
    return (b - a) * f(a)


# АСТ 0
def quadrature_formula_of_right_rect(f, a: float, b: float):
    return (b - a) * f(b)


# АСТ 1
def quadrature_formula_of_inter_rect(f, a: float, b: float):
    return (b - a) * f((a + b) / 2)


# АСТ 1
def quadrature_formula_of_trap(f, a: float, b: float):
    return (b - a) * (f(a) + f(b)) / 2


# АСТ 3
def quadrature_formula_of_simp(f, a: float, b: float):
    return (b - a) * (f(a) + 4 * f((a + b) / 2) + f(b)) / 6


# АСТ 3
def quadrature_formula_of_3_8(f, a: float, b: float):
    h = (b - a) / 3
    return (b - a) * (f(a) + 3 * f(a + h) + 3 * f(a + 2 * h) + f(b)) / 8


def print_conditions(a: float, b: float):
    print()
    print(Fore.GREEN + "Задание №4.1.")
    print(Fore.GREEN + "Приближённое вычисление интеграла по квадратурным формулам.")
    print()
    print(Fore.CYAN + "Пределы интегрирования:")
    print("a =", a)
    print("b =", b)
    print()
    print(Fore.CYAN + "Рассматриваемые функции:")
    print("1) 42")
    print("2) 2x + 42")
    print("3) 3x^2 + 2x + 42")
    print("4) 4x^2 + 3x^2 + 2x + 42")
    print("5) exp(x)")
    print("6) sin(x)")


def print_menu():
    print()
    print(Fore.CYAN + "Меню действий:", end="\n\n")
    print("0 - Вывести исходные данные и параметры задачи")
    print("1 - Изменить пределы интегрирования")
    print("2 - Провести вычисления")
    print("3 - Очистить консоль")
    print("4 - Завершить работу")


def integration_of_function(f, a: float, b: float):
    result_of_integration, upper_boundary_of_error = integrate.quad(f, a, b)
    return result_of_integration


functions = [
    ("42", lambda x: x * 0 + 42),
    ("2x + 42", lambda x: 2 * x + 42),
    ("3x^2 + 2x + 42", lambda x: 3 * x ** 2 + 2 * x + 42),
    ("4x^2 + 3x^2 + 2x + 42", lambda x: 4 * x ** 2 + 3 * x ** 2 + 2 * x + 42),
    ("exp(x)", lambda x: math.exp(x)),
    ("sin(x)", lambda x: math.sin(x)),
]

quadratures_formulas_name = [
    "КФ левого прямоугольника",
    "КФ правого прямоугольника",
    "КФ среднего прямоугольника",
    "КФ трапеции",
    "КФ Симпсона",
    "КФ 3/8",
]


def main():
    init(autoreset=True)
    a = 0
    b = 1
    isExit = False

    print_menu()
    while not isExit:
        print()
        print("-" * 120)
        print()
        print(Fore.BLUE + "Выполнить команду (Вызов меню - 5): ", end="")
        try:
            commad_number = int(input())
        except:
            commad_number = 6

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
        elif commad_number == 2:
            headers = [
                "Название квадратурной формулы",
                "Приближенное значение J(n)",
                "Значение фактической ошибки |J(n) - J|",
            ]

            for function_name, function in functions:
                result_list = []
                error_list = []

                results_of_integrations = integration_of_function(function, a, b)

                left_rect = quadrature_formula_of_left_rect(function, a, b)
                right_rect = quadrature_formula_of_right_rect(function, a, b)
                inter_rect = quadrature_formula_of_inter_rect(function, a, b)
                trap = quadrature_formula_of_trap(function, a, b)
                simp = quadrature_formula_of_simp(function, a, b)
                qd_3_8 = quadrature_formula_of_3_8(function, a, b)

                result_list.extend([left_rect, right_rect, inter_rect, trap, simp, qd_3_8])

                error_list.extend(
                    [
                        abs(left_rect - results_of_integrations),
                        abs(right_rect - results_of_integrations),
                        abs(inter_rect - results_of_integrations),
                        abs(trap - results_of_integrations),
                        abs(simp - results_of_integrations),
                        abs(qd_3_8 - results_of_integrations),
                    ]
                )

                print("\n\n")
                print(Fore.GREEN + f"Выбранная функция: {function_name}")
                print(Fore.GREEN + f"Точное значение интеграла J: {results_of_integrations}")

                table = zip(quadratures_formulas_name, result_list, error_list)
                print("\n" + tabulate(table, headers, floatfmt=".15e", tablefmt="grid"))

        elif commad_number == 3:
            os.system("cls" if os.name == "nt" else "clear")
        elif commad_number == 4:
            sys.exit()
        elif commad_number == 5:
            os.system("cls" if os.name == "nt" else "clear")
            print_menu()
        else:
            print(Fore.RED + "\nЯ не знаю такой команды :(")


if __name__ == "__main__":
    main()
