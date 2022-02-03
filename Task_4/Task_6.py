import sys
import os
import math
import numpy as np
import scipy.integrate as integrate
from colorama import init, Fore
from tabulate import tabulate

np.set_printoptions(precision=20, floatmode="fixed")

# Тестовая функция f
def f(x):
    return math.sin(x)


# Соответствующий вес p
def p(x):
    return math.exp(-x)


# Произведение f на p
def pf(x):
    return math.sin(x) * math.exp(-x)


# Первообразная от f
def F(x):
    return -math.cos(x)


# Первообразная от p
def P(x):
    return -math.exp(-x)


def integration_of_function(f, a: float, b: float):
    result_of_integration, upper_boundary_of_error = integrate.quad(f, a, b)
    return result_of_integration


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
def secant_method(f, left_border, right_border, n, eps=1e-13):
    nodes = []
    h = (right_border - left_border) / (2 * n + (n % 2) + 2)

    # Секущая
    for i in range(0, 2 * n + (n % 2) + 2):
        x0 = left_border + i * h
        x1 = left_border + (i + 1) * h

        # Сохраняем начальные значения
        fx0 = f(x0, n)
        fx1 = f(x1, n)

        if fx0 * fx1 < 0:
            while abs(fx1) > eps:
                # Выполняем расчёт
                x2 = (x0 * fx1 - x1 * fx0) / (fx1 - fx0)
                # Сдвиг переменных (подготовка к следующему циклу)
                x0, x1 = x1, x2
                fx0, fx1 = fx1, f(x2, n)

            nodes.append(x1)

    return nodes


# Узлы и коэффициенты подобной КФ
def similar_quadrature_formula(a, b, nodes, coefficients, f):
    n_nodes = nodes.copy()
    n_coefficients = coefficients.copy()

    for i in range(0, len(n_nodes)):
        n_nodes[i] = 0.5 * (a + b + (b - a) * n_nodes[i])

    for i in range(0, len(n_coefficients)):
        n_coefficients[i] = ((b - a) / 2) * n_coefficients[i]

    J = sum([f(n_nodes[i]) * n_coefficients[i] for i in range(0, len(n_nodes))])

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


# Момент весовой функции
def moment_value(a, b, k):
    return integrate.quad(lambda x: p(x) * x ** k, a, b)[0]


# Коэффициенты ортогонального многочлена
def orthogonal_polynomial(a, b, N):
    moments_list = []

    for i in range(0, 2 * N):
        moments_list.append(moment_value(a, b, i))

    a = np.array([[moments_list[i - j] for j in range(0, N)] for i in range(N - 1, 2 * N - 1)])
    b = np.array([-moments_list[i] for i in range(N, 2 * N)])

    return np.linalg.solve(a, b)


# Коэффициенты КФ
def similar_quadrature_coefficients(roots, moments, N):
    coefficients_list = []
    coefficients_list.append([1 for i in range(0, N)])
    coefficients_list.append(roots.copy())

    for i in range(2, N):
        coefficients_list.append([(x ** i) for x in roots])

    a = np.array([li for li in coefficients_list])
    b = np.array([moments[i] for i in range(0, N)])

    return np.linalg.solve(a, b)


def print_conditions(a, b):
    print()
    print(Fore.GREEN + "Задание №6. Вариант #13")
    print(Fore.GREEN + "Приближённое вычисление интегралов при помощи квадратурных формул")
    print(Fore.GREEN + "Наивысшей Алгебраической Степени Точности (КФ НАСТ)")
    print()
    print(Fore.CYAN + "Исходные данные и параметры задачи:")
    print(f"a = {a}")
    print(f"b = {b}")
    print("f(x) = sin(x)")
    print("p(x) = e^(-x)")


def print_menu():
    print()
    print(Fore.CYAN + "Меню действий:", end="\n\n")
    print("0 - Вывести исходные данные и параметры задачи")
    print("1 - Изменить исходные данные и параметры задачи")
    print("2 - Вычисление при помощи КФ типа Гаусса (КФ НАСТ)")
    print("3 - Вычисление при помощи СКФ Гаусса")
    print("4 - Осуществить проверку точности на многочлене наивысшей степени")
    print("5 - Очистить консоль")
    print("6 - Завершить работу")


def main():
    init(autoreset=True)

    a = 0
    b = 1
    m = 10
    integral_r = integration_of_function(lambda x: pf(x), a, b)
    h = (b - a) / m
    isExit = False

    print_menu()
    print()
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

            h = (b - a) / m
            integral_r = integration_of_function(lambda x: pf(x), a, b)

        elif commad_number == 3:
            # Задача 2 (СКФ Гаусса)
            try:
                N = int(input("Введите N (число узлов): "))
            except:
                N = int(3)
            try:
                m = int(input("Введите m (число промежутков разбиения): "))
            except:
                m = int(10)

            h = (b - a) / m
            integral_r = integration_of_function(lambda x: pf(x), a, b)

            init_nodes = secant_method(lejandre_polynomial, -1, 1, N)
            init_coefficients = get_coefficients(init_nodes, N)
            full_integral = sum(
                [
                    similar_quadrature_formula(a + i * h, a + (i + 1) * h, init_nodes, init_coefficients, pf)[2]
                    for i in range(0, m)
                ]
            )

            sim_nodes, sim_coefficients, integral = similar_quadrature_formula(-1, 1, init_nodes, init_coefficients, pf)

            print(Fore.CYAN + f"\nN = {N}, m = {m}")
            print(Fore.GREEN + f"\nУзлы и коэффициенты СКФ Гаусса (на [-1, 1]):")
            print_table(sim_nodes, sim_coefficients, N)
            sim_nodes, sim_coefficients, integral = similar_quadrature_formula(a, b, init_nodes, init_coefficients, pf)
            print(Fore.GREEN + f"\nI точн. =", integral_r)
            # print(Fore.GREEN + "\nКФ Гаусса:")
            # print(f"I прибл. кф = {integral}")
            # print(f"|I точн. - I прибл. кф| = {abs(integral_r - integral)}")
            print(Fore.GREEN + "\nСКФ Гаусса:")
            print(f"I прибл. скф = {full_integral}")
            print(f"|I точн. - I прибл. скф| = {abs(integral_r - full_integral)}")

        elif commad_number == 2:
            # Задача 1 (КФ НАСТ)
            try:
                N = int(input("\nВведите N (квадратурной формулы типа Гаусса): "))
            except:
                N = int(3)

            h = (b - a) / m
            integral_r = integration_of_function(lambda x: pf(x), a, b)

            init_nodes = secant_method(lejandre_polynomial, -1, 1, N)
            init_coefficients = get_coefficients(init_nodes, N)
            full_integral = sum(
                [
                    similar_quadrature_formula(a + i * h, a + (i + 1) * h, init_nodes, init_coefficients, pf)[2]
                    for i in range(0, m)
                ]
            )

            print(Fore.CYAN + f"\nN = {N}")
            print(Fore.GREEN + "\nМоменты весовой функции:")
            for i in range(0, 2 * N):
                print(f"m_{i}\t=\t{moment_value(a, b, i)}")

            print(Fore.GREEN + "\nОртогональный многочлен:")
            ort_pol = orthogonal_polynomial(a, b, N)
            print(f"x^{N}", end=" ")
            for i in range(0, N):
                if ort_pol[i] >= 0:
                    print(f"+ {round(ort_pol[i], 16)}*x^{N - i - 1}", end=" ")
                else:
                    print(f"- {round(abs(ort_pol[i]), 16)}*x^{N - i - 1}", end=" ")
            print()

            headers = ["№", "Узел", "Коэффициент"]
            full_ort_pol = [1]
            full_ort_pol.extend(ort_pol.copy())
            roots = np.roots(full_ort_pol)

            quadrature_formula_coefficients = similar_quadrature_coefficients(
                roots, [moment_value(a, b, i) for i in range(0, N)], N
            )

            count = []
            for i in range(1, len(roots) + 1):
                count.append(i)

            print(Fore.GREEN + f"\nУзлы и коэффициенты КФ НАСТ (на [{a}, {b}]):")
            table = zip(count, roots, quadrature_formula_coefficients)
            print("\n" + tabulate(table, headers, floatfmt=".20e", tablefmt="grid"))
            print(Fore.GREEN + "\nChecksum:", sum(quadrature_formula_coefficients))

            print(Fore.GREEN + f"\nI точн. =", integral_r)

            print(Fore.GREEN + "\nКФ НАСТ:")
            nast_int = sum([f(roots[i]) * quadrature_formula_coefficients[i] for i in range(0, N)])
            print(f"I наст. = {nast_int}")
            print(f"|I наст. - I| = {abs(nast_int - integral_r)}")

        elif commad_number == 4:
            print(Fore.GREEN + "\nПроверка на многочлене степени 2N - 1:")
            m_max = moment_value(a, b, 2 * N - 1)
            kf_pm = sum([(roots[i] ** (2 * N - 1)) * quadrature_formula_coefficients[i] for i in range(0, N)]) - (
                sum([(roots[i] ** (2 * N - 1)) * quadrature_formula_coefficients[i] for i in range(0, N)]) - m_max
            )
            print(f"m_{2*N - 1} = {m_max}")
            print(f"J_m = {kf_pm}")
            print(f"|m_{2*N - 1} - J_m| = {abs(kf_pm - m_max)}")

        elif commad_number == 5:
            os.system("cls" if os.name == "nt" else "clear")

        elif commad_number == 6:
            sys.exit()

        elif commad_number == 7:
            os.system("cls" if os.name == "nt" else "clear")
            print_menu()

        else:
            print()
            print(Fore.RED + "\nЯ не знаю такой команды :(")
            print()


if __name__ == "__main__":
    main()
