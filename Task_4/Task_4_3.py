import sys
import os
import math
import scipy.integrate as integrate
from colorama import init, Fore
from tabulate import tabulate

from Task_4_2 import *


def clarify_by_runge(l, h_l, h, function, a, b, n, ast, number):

    if ast == 0 and number == 1:
        Jh = сompound_quadrature_formula_of_left_rect(function, a, b, n, h)
        Jhl = сompound_quadrature_formula_of_left_rect(function, a, b, n * l, h_l)
        r = ast + 1

    if ast == 0 and number == 2:
        Jh = сompound_quadrature_formula_of_right_rect(function, a, b, n, h)
        Jhl = сompound_quadrature_formula_of_right_rect(function, a, b, n * l, h_l)
        r = ast + 1

    if ast == 1 and number == 3:
        Jh = сompound_quadrature_formula_of_inter_rect(function, a, b, n, h)
        Jhl = сompound_quadrature_formula_of_inter_rect(function, a, b, n * l, h_l)
        r = ast + 1

    if ast == 1 and number == 4:
        Jh = сompound_quadrature_formula_of_trap(function, a, b, n, h)
        Jhl = сompound_quadrature_formula_of_trap(function, a, b, n * l, h_l)
        r = ast + 1

    if ast == 3 and number == 5:
        Jh = сompound_quadrature_formula_of_simp(function, a, b, n, h)
        Jhl = сompound_quadrature_formula_of_simp(function, a, b, n * l, h_l)
        r = ast + 1

    if ast == 3 and number == 6:
        Jh = сompound_quadrature_formula_of_3_8(function, a, b, n, h)
        Jhl = сompound_quadrature_formula_of_3_8(function, a, b, n * l, h_l)
        r = ast + 1

    return (l ** r * Jhl - Jh) / (l ** r - 1)


def print_conditions(a: float, b: float, n: int, h, l, h_l):
    print()
    print(Fore.GREEN + "Задание №4.3.")
    print(Fore.GREEN + "Приближённое вычисление интеграла по составным квадратурным формулам.")
    print()
    print(Fore.CYAN + "Исходные данные и параметры задачи:")
    print("a =", a)
    print("b =", b)
    print("m =", n)
    print("l =", l)
    print(f"h = (b-a)/m = {h}")
    print(f"h/l = (b-a)/(m*l) = {h_l}")
    print()
    print(Fore.CYAN + "Рассматриваемые функции:")
    print("1) 42")
    print("2) 2x + 42")
    print("3) 3x^2 + 2x + 42")
    print("4) 4x^2 + 3x^2 + 2x + 42")
    print("5) 5x^4 + 4x^3 + 3x^2 + 2x + 42")
    print("6) exp(x)")
    print("7) sin(x)")
    print("8) sin(x) + x^3 - 9 * x + 3")


def print_menu():
    print()
    print(Fore.CYAN + "Меню действий:", end="\n\n")
    print("0 - Вывести исходные данные и параметры задачи")
    print("1 - Изменить исходные данные и параметры задачи")
    print("2 - Провести вычисления")
    print("3 - Очистить консоль")
    print("4 - Завершить работу")


def main():
    init(autoreset=True)
    a = 0
    b = 1
    n = 10
    l = 2
    h = (b - a) / n
    h_l = (b - a) / (n * l)
    isExit = False
    have_derivative = False

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
            print_conditions(a, b, n, h, l, h_l)
        elif commad_number == 1:
            try:
                a = float(input("Введите значение левой границы интегрирования (a): "))
            except:
                a = float(0)
            try:
                b = float(input("Введите значение правой границы интегрирования (b): "))
            except:
                b = float(1)
            try:
                n = int(input("Введите число разбиений промежутка интегрирования: "))
            except:
                n = int(10)
            try:
                l = int(input("Увеличить m в l раз(-а): "))
            except:
                l = int(2)

            h = (b - a) / n
            h_l = (b - a) / (n * l)
            print(f"h = (b-a)/m = {h}")
            print(f"h/l = (b-a)/(m*l) = {h_l}")
        elif commad_number == 2:
            headers = [
                "Название СКФ",
                "J(h)",
                "|J - J(h)|",
                "J(h/l)",
                "|J - J(h/l)|",
                "J_r",
                "|J - J_r|",
            ]

            for function_name, function in functions:

                result_list = []
                error_list = []
                result_list_l = []
                error_list_l = []
                clar_list = []
                error_clar_list = []

                results_of_integrations = integration_of_function(function, a, b)

                # АСТ 0 (алгебраическая степень точности)
                left_rect = сompound_quadrature_formula_of_left_rect(function, a, b, n, h)
                # АСТ 0 
                right_rect = сompound_quadrature_formula_of_right_rect(function, a, b, n, h)
                # АСТ 1
                inter_rect = сompound_quadrature_formula_of_inter_rect(function, a, b, n, h)
                # АСТ 1
                trap = сompound_quadrature_formula_of_trap(function, a, b, n, h)
                # АСТ 3
                simp = сompound_quadrature_formula_of_simp(function, a, b, n, h)
                # АСТ 3
                qd_3_8 = сompound_quadrature_formula_of_3_8(function, a, b, n, h)

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


                left_rect_l = сompound_quadrature_formula_of_left_rect(function, a, b, n * l, h_l)
                right_rect_l = сompound_quadrature_formula_of_right_rect(function, a, b, n * l, h_l)
                inter_rect_l = сompound_quadrature_formula_of_inter_rect(function, a, b, n * l, h_l)
                trap_l = сompound_quadrature_formula_of_trap(function, a, b, n * l, h_l)
                simp_l = сompound_quadrature_formula_of_simp(function, a, b, n * l, h_l)
                qd_3_8_l = сompound_quadrature_formula_of_3_8(function, a, b, n * l, h_l)

                result_list_l.extend([left_rect_l, right_rect_l, inter_rect_l, trap_l, simp_l, qd_3_8_l])

                error_list_l.extend(
                    [
                        abs(left_rect_l - results_of_integrations),
                        abs(right_rect_l - results_of_integrations),
                        abs(inter_rect_l - results_of_integrations),
                        abs(trap_l - results_of_integrations),
                        abs(simp_l - results_of_integrations),
                        abs(qd_3_8_l - results_of_integrations),
                    ]
                )

                left_rect_clar = clarify_by_runge(l, h_l, h, function, a, b, n, 0, 1)
                right_rect_clar = clarify_by_runge(l, h_l, h, function, a, b, n, 0, 2)
                inter_rect_clar = clarify_by_runge(l, h_l, h, function, a, b, n, 1, 3)
                trap_clar = clarify_by_runge(l, h_l, h, function, a, b, n, 1, 4)
                simp_clar = clarify_by_runge(l, h_l, h, function, a, b, n, 3, 5)
                qd_3_8_clar = clarify_by_runge(l, h_l, h, function, a, b, n, 3, 6)

                clar_list.extend([left_rect_clar, right_rect_clar, inter_rect_clar, trap_clar, simp_clar, qd_3_8_clar])

                error_clar_list.extend(
                    [
                        abs(left_rect_clar - results_of_integrations),
                        abs(right_rect_clar - results_of_integrations),
                        abs(inter_rect_clar - results_of_integrations),
                        abs(trap_clar - results_of_integrations),
                        abs(simp_clar - results_of_integrations),
                        abs(qd_3_8_clar - results_of_integrations),
                    ]
                )

                print("\n\n")
                print(Fore.GREEN + f"Выбранная функция: {function_name}")
                print(Fore.GREEN + f"Точное значение интеграла J: {results_of_integrations}")

                table = zip(
                    quadratures_formulas_name,
                    result_list,
                    error_list,
                    result_list_l,
                    error_list_l,
                    clar_list,
                    error_clar_list,
                )
                print("\n" + tabulate(table, headers, floatfmt=".7e", tablefmt="grid"))

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
