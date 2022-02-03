import sys
import os
import math
import scipy.integrate as integrate
from colorama import init, Fore
from tabulate import tabulate


# АСТ 0 (алгебраическая степень точности)
def сompound_quadrature_formula_of_left_rect(f, a, b, n, h):
    sum = 0
    return_value = None
    m = 0

    for i in range(1, n + 1):
        sum += f(a + (i - 1) * h)

    # if have_derivative:
    #     m = find_max(derivative_of_function[0], a, n, h) * (b - a)
    #     return_value = 1 / 2 * m * math.pow(b - a, 2) / n

    return sum * h


# АСТ 0
def сompound_quadrature_formula_of_right_rect(f, a, b, n, h):
    sum = 0
    return_value = None
    m = 0

    for i in range(1, n + 1):
        sum += f(a + h + (i - 1) * h)

    # if have_derivative:
    #     m = find_max(derivative_of_function[0], a, n, h) * (b - a)
    #     return_value = 1 / 2 * m * math.pow(b - a, 2) / n

    return sum * h


# АСТ 1
def сompound_quadrature_formula_of_inter_rect(f, a, b, n, h):
    sum = 0
    return_value = None
    m = 0

    for i in range(1, n + 1):
        sum += f(a + h / 2 + (i - 1) * h)

    # if have_derivative:
    #     m = find_max(derivative_of_function[1], a, n, h) * (b - a)
    #     return_value = 1 / 24 * m * math.pow((b - a), 3) / math.pow(n, 2)

    return sum * h


# АСТ 1
def сompound_quadrature_formula_of_trap(f, a, b, n, h):
    sum = 0
    return_value = None
    m = 0

    for i in range(1, n + 1):
        sum += f(a + (i - 1) * h) + f(a + h * i)

    # if have_derivative:
    #     m = find_max(derivative_of_function[1], a, n, h) * (b - a)
    #     return_value = 1 / 12 * m * math.pow((b - a), 3) / math.pow(n, 2)

    return sum * h / 2


# АСТ 3
def сompound_quadrature_formula_of_simp(f, a, b, n, h):
    sum = 0
    return_value = None
    m = 0

    for i in range(1, n + 1):
        sum += f(a + (i - 1) * h) + 4 * f(a + h / 2 * (2 * i - 1)) + f(a + h * i)

    # if have_derivative:
    #     m = find_max(derivative_of_function[0], a, n, h) * (b - a)
    #     return_value = 1 / 2880 * m * math.pow((b - a), 5) / math.pow(n, 4)

    return sum * h / 6


# АСТ 3
def сompound_quadrature_formula_of_3_8(f, a, b, n, h):
    sum = 0
    return_value = None
    m = 0

    for i in range(1, n + 1):
        sum += f(a + (i - 1) * h) + 3 * f(a + i * h - 2 * h / 3) + 3 * f(a + i * h - h / 3) + f(a + h * i)

    # if have_derivative:
    #     m = find_max(derivative_of_function[0], a, n, h) * (b - a)
    #     return_value = 1 / 6480 * m * math.pow((b - a), 5) / math.pow(n, 4)

    return sum * h / 8


def find_max(f, a, n, h):
    local_maximum = 0

    for i in range(1, n + 1):
        local_maximum = max(local_maximum, abs(f(a + h * i)))

    return local_maximum


def print_conditions(a: float, b: float, n: int, h):
    print()
    print(Fore.GREEN + "Задание №4.2.")
    print(Fore.GREEN + "Приближённое вычисление интеграла по составным квадратурным формулам.")
    print()
    print(Fore.CYAN + "Исходные данные и параметры задачи:")
    print("a =", a)
    print("b =", b)
    print("m =", n)
    print(f"h = (b-a)/m = {h}")
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


def integration_of_function(f, a: float, b: float):
    result_of_integration, upper_boundary_of_error = integrate.quad(f, a, b)
    return result_of_integration


functions = [
    ("42", lambda x: x * 0 + 42),
    ("2x + 42", lambda x: 2 * x + 42),
    ("3x^2 + 2x + 42", lambda x: 3 * x ** 2 + 2 * x + 42),
    ("4x^2 + 3x^2 + 2x + 42", lambda x: 4 * x ** 2 + 3 * x ** 2 + 2 * x + 42),
    ("5x^4 + 4x^3 + 3x^2 + 2x + 42", lambda x: 5 * x ** 4 + 4 * x ** 3 + 3 * x ** 2 + 2 * x + 42),
    ("exp(x)", lambda x: math.exp(x)),
    ("sin(x)", lambda x: math.sin(x)),
    ("sin(x) + x^3 - 9 * x + 3", lambda x: math.sin(x) + x ** 3 - 9 * x + 3),
]

derivative_of_function = [
    # Первая производная
    (lambda x: -9 + 3 * x ** 2 + math.cos(x)),
    # Вторая производная
    (lambda x: 6 * x - math.sin(x)),
    # Четвёртая производная
    (lambda x: math.sin(x)),
]

quadratures_formulas_name = [
    "СКФ левого прямоугольника",
    "СКФ правого прямоугольника",
    "СКФ среднего прямоугольника",
    "СКФ трапеции",
    "СКФ Симпсона",
    "СКФ 3/8",
]


def main():
    init(autoreset=True)
    a = 0
    b = 1
    n = 10
    h = (b - a) / n
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
            print_conditions(a, b, n, h)
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

            h = (b - a) / n
            print(f"h = (b-a)/m = {h}")
        elif commad_number == 2:
            headers = [
                "Название СКФ",
                "J(h)",
                "|J(h) - J|",
                "Значение теоретической погрешности",
            ]

            number_of_function = 1
            have_derivative = False

            for function_name, function in functions:

                if number_of_function == 8:
                    have_derivative = True

                result_list = []
                error_list = []
                theor_error_list = []

                results_of_integrations = integration_of_function(function, a, b)

                left_rect, left_rect_theor_error = сompound_quadrature_formula_of_left_rect(
                    function, a, b, n, h, have_derivative
                )
                right_rect, right_rect_theor_error = сompound_quadrature_formula_of_right_rect(
                    function, a, b, n, h, have_derivative
                )
                inter_rect, inter_rect_theor_error = сompound_quadrature_formula_of_inter_rect(
                    function, a, b, n, h, have_derivative
                )
                trap, trap_theor_error = сompound_quadrature_formula_of_trap(function, a, b, n, h, have_derivative)
                simp, simp_theor_error = сompound_quadrature_formula_of_simp(function, a, b, n, h, have_derivative)
                qd_3_8, qd_3_8_theor_error = сompound_quadrature_formula_of_3_8(function, a, b, n, h, have_derivative)

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

                theor_error_list.extend(
                    [
                        left_rect_theor_error,
                        right_rect_theor_error,
                        inter_rect_theor_error,
                        trap_theor_error,
                        simp_theor_error,
                        qd_3_8_theor_error,
                    ]
                )

                print("\n\n")
                print(Fore.GREEN + f"Выбранная функция: {function_name}")
                print(Fore.GREEN + f"Точное значение интеграла J: {results_of_integrations}")

                table = zip(quadratures_formulas_name, result_list, error_list, theor_error_list)
                print("\n" + tabulate(table, headers, floatfmt=".15e", tablefmt="grid"))

                number_of_function += 1

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
