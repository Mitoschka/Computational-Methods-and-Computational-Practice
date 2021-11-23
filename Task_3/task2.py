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


class Root:
    def __init__(self, arg, value):
        self.arg = arg
        self.value = value
        self.distance = None

    def set_distance(self, new_arg):
        self.distance = abs(self.arg - new_arg)


def func(x):
     return 2 * math.sin(x) - pow(x, 2) / 2


def tabulate_value(a, b, m, func, reversed=False):
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
    for k in range(n + 1):  # суммирование l_{kn} по k
        res_k = 1
        for i in range(n + 1):  # умножение (x - x_i) / (x_k - x_i) по i
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
            diff_value = (diff_table[i + 1][-1] - diff_table[i][-1]) / (table[i + j + 1].arg - table[i].arg)
            diff_table[i].append(diff_value)

    for k in range(n + 1):
        res_x_multiply = 1
        for j in range(k):
            res_x_multiply *= (x - table[j].arg)
        res += diff_table[0][k] * res_x_multiply

    print(diff_table)
    return res


def print_table(table, show_distance=False, reversed=False):
    if show_distance:
        if reversed:
            print("%-12s%-12s\033[96m%-12s" % ("f(x)", "x", "distance"))
        else:
            print("%-12s%-12s\033[96m%-12s" % ("x", "f(x)", "distance"))

        print("%-12s%-12s%-12s" % ("--------", "--------", "--------"))

        for root in table:
            print("\033[0m%-12.9f%-12.9f\033[96m%-12.9f" % (root.arg, root.value, root.distance))
    else:
        if reversed:
            print("%-9s%-9s" % ("f(x)", "x"))
        else:
            print("%-9s%-9s" % ("x", "f(x)"))

        print("%-9s%-9s" % ("--------", "--------"))

        for root in table:
            print("%-9f%-9f" % (root.arg, root.value))


def solve_request(table):
    x_0 = float(input("\n\033[1mВведите x: \033[0m"))

    for root in table:
        root.set_distance(x_0)

    sorted_table = sorted(table, key=lambda o: o.distance)
    print("\nОтсортированная таблица:")
    print_table(sorted_table, show_distance=True)

    n = int(input("\n\033[0m\033[1mВведите степень многочлена n < %d: \033[0m" % m))

    while n >= m:
        n = int(input("\033[91mНедопустимое значение! \033[0m\033[1mВведите степень многочлена n <= %d: \033[0m" % m))

    lagrange_res = lagrange(sorted_table, x_0, n)
    newton_res = newton(sorted_table, x_0, n)

    print("Lagrange: \033[92m%.24f\033[0m (±%.24f)" % (lagrange_res, abs(lagrange_res - func(x_0))))

    print("Newton: \033[92m%.24f\033[0m  (±%.24f)" % (newton_res, abs(newton_res - func(x_0))))


if __name__ == '__main__':
    a = -1
    b = 4

    print("Задача алгебраического интерполирования\n\n"
          "Вид уравнения: 2 * sin(x) - x^2 / 2 (вариант 8)\n"
          "отрезок: [%f, %f]\n" % (a, b))

    m = int(input("\033[1mВведите число значений в таблице (m+1): \033[0m"))

    table = tabulate_value(a, b, m - 1, func)
    print_table(table)

    while True:
        solve_request(table)
        print("\nРешить заново?")



