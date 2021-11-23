import math


class Root:
    def __init__(self, arg, value):
        self.arg = arg
        self.value = value
        self.d1 = -1
        self.d2 = -1


def func(x):
    return math.exp(6 * x)


def funcD1(x):
    return math.exp(6 * x) * 6


def funcD2(x):
    return math.exp(6 * x) * 36


def tabulate_value(a, h, m, func, reversed=False):
    table = []
    for i in range(m + 1):
        arg = a + i * h
        root = Root(arg, func(arg))
        table.append(root)
    return table


def findD1(table, h):
    table[0].d1 = (-3 * table[0].value + 4 * table[1].value - table[2].value) / (2 * h)
    table[len(table) - 1].d1 = (3 * table[len(table) - 1].value - 4 * table[len(table) - 2].value + table[
        len(table) - 3].value) / (2 * h)

    for i in range(1, len(table) - 1):
        table[i].d1 = (table[i + 1].value - table[i - 1].value) / (2 * h)


def findD2(table, h):
    for i in range(1, len(table) - 1):
        table[i].d2 = (table[i + 1].value - 2 * table[i].value + table[i - 1].value) / (math.pow(h, 2))


def print_table(table):
    print("%-15s%-15s%-15s%-15s%-15s%-15s" % ("x", "f(x)", "f'(x)", "err(f'(x))", "f''(x)", "err(f''(x))"))

    print("%-15s%-15s%-15s%-15s%-15s%-15s" % ("--------", "--------", "--------", "--------", "--------", "--------"))

    for i in range(len(table)):
        root = table[i]
        if i == 0 or i == len(table) - 1:
            print("%-15f%-15f%-15f%-15f%-15s%-15s" % (
                root.arg, root.value, root.d1, abs(root.d1 - funcD1(root.arg)), "None", "None"))
        else:
            print("%-15f%-15f%-15f%-15f%-15f%-15f" % (
            root.arg, root.value, root.d1, abs(root.d1 - funcD1(root.arg)), root.d2, abs(root.d2 - funcD2(root.arg))))


if __name__ == '__main__':
    print("Нахождение производных таблично-заданной функции по формулам численного дифференцирования\n\n"
          "Вид уравнения: e^6x (вариант 8)\n")

    while True:
        a = float(input("\033[1mВведите a (начало отрезка): \033[0m"))
        h = float(input("\033[1mВведите h (величина отрезка): \033[0m"))
        m = int(input("\033[1mВведите кол-во значений (m+1): \033[0m"))

        table = tabulate_value(a, h, m, func)
        findD1(table, h)
        findD2(table, h)

        print_table(table)

        print("\nРешить заново?")
