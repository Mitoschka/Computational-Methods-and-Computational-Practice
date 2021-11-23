from task2 import tabulate_value, lagrange, print_table
from task1 import bisect, root_division
import math


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def func(x):
    return 2 * math.sin(x) - pow(x, 2) / 2


def solve_lagrange(a, b, m, f, n):
    table = tabulate_value(a, b, m - 1, func, reversed=True)

    for root in table:
        root.set_distance(f)

    sorted_table = sorted(table, key=lambda o: o.distance)
    # print("\nОтсортированная таблица:")
    # print_table(sorted_table, show_distance=True, reversed=True)

    lagrange_res = lagrange(sorted_table, f, n)
    print("\n\033[1mLagrange: x = \033[92m%.24f\033[0m \n|f(x) - F|  = %.24f" % (lagrange_res, abs(func(lagrange_res) - f)))


def lagrange_func(table, x_0, n):
    for root in table:
        root.set_distance(x_0)

    sorted_table = sorted(table, key=lambda o: o.distance)
    lagrange_res = lagrange(sorted_table, x_0, n)

    return lagrange_res


def solve_bisect(a, b, table, f, n, eps):
    sections = root_division(a, b, lambda x: lagrange_func(table, x, n) - f, n=10)
    ans = bisect(sections[0][0], sections[0][1], eps, lambda x: lagrange_func(table, x, n) - f)

    print("\n\033[1mBisect:  x = \033[92m%.24f\033[0m \n|f(x) - F| = %.24f" % (ans.solution, abs(func(ans.solution) - f)))



if __name__ == '__main__':
    a = 0.2
    b = 0.7

    print("Задача обратного алгебраического интерполирования\n\n"
          "Вид уравнения: 2 * sin(x) - x^2 / 2 (вариант 8)\n"
          "отрезок: [%f, %f]\n" % (a, b))

    m = int(input("\033[1mВведите число значений в таблице (m+1): \033[0m"))
    table = tabulate_value(a, b, m - 1, func)

    while True:
        print_table(table)
        f = float(input("\n\033[1mВведите F: \033[0m"))
        n1 = int(input("\033[0m\033[1mВведите степень многочлена n1 < %d: \033[0m" % m))
        while n1 >= m:
            n1 = int(
                input("\033[91mНедопустимое значение! \033[0m\033[1mВведите степень многочлена n1 < %d: \033[0m" % m))
        n2 = int(input("\033[0m\033[1mВведите степень многочлена n1 < %d: \033[0m" % m))

        while n2 >= m:
            n2 = int(
                input("\033[91mНедопустимое значение! \033[0m\033[1mВведите степень многочлена n2 < %d: \033[0m" % m))
        try:
            eps = float(input("\033[1mВведите eps (по умолчанию 10^-8):"))
        except:
            eps = 0.00000001

        solve_lagrange(a, b, m, f, n1)
        solve_bisect(a, b, table, f, n2, eps)

        input("\nРешить заново?")

