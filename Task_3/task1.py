import math


class Solution:
    def __init__(self, solution, steps, init_approx, abs_error, func_solve):
        self.solution = solution
        self.steps = steps
        self.init_approx = init_approx
        self.abs_error = abs_error
        self.func_solve = func_solve
        self.is_found = True
        self.err_name = None


class UnsolvedSolution(Solution):
    def __init__(self, err_name):
        self.is_found = False
        self.err_name = err_name


def func(x):
    return 4 * math.cos(x) + 0.3 * x


def d_func(x):
    return -4 * math.sin(x) + 0.3


def root_division(a, b, func, n = 50): # деление корней
    sections = []

    step = 0
    h = (b - a) / n
    x_0 = a

    while x_0 <= b:
        x_1 = a + (step + 1) * h
        y_0 = func(x_0)
        y_1 = func(x_1)
        if y_0 * y_1 <= 0:
            sections.append([x_0, x_1])

        x_0 = x_1
        step += 1

    return sections


def bisect(a, b, eps, func): # приближение методом бисекции
    step = 0
    x = (a + b) / 2
    x_0 = 0

    while b - a > 2 * eps:
        step += 1
        x_0 = x
        x = (a + b) / 2
        if func(a) * func(x) <= 0:
            b = x
        else:
            a = x
    return Solution(solution=x,
                    steps=step,
                    init_approx=[(a + b) / 2],
                    abs_error=abs(x - x_0),
                    func_solve=func(x))


def newton(a, b, eps, func, d_func, iter = 100): # приближение методом Ньютона
    step = 0
    x_0 = (a + b) / 2
    x = x_0 - func(x_0) / d_func(x_0)

    while abs(x - x_0) > eps and step < iter:
        step += 1
        x_0 = x
        x = x_0 - func(x_0) / d_func(x_0)

    if step == iter:
        return UnsolvedSolution("LimitExceeded")
    else:
        return Solution(solution=x,
                        steps=step,
                        init_approx=[(a + b) / 2],
                        abs_error=abs(x - x_0),
                        func_solve=func(x))


def newton_m(a, b, eps, func, d_func, iter = 100): # приближение модифицированным методом Ньютона
    step = 0
    x_0 = (a + b) / 2
    x = x_0 - func(x_0) / d_func(x_0)

    while abs(x - x_0) > eps and step < iter:
        step += 1
        x_0 = x
        x = x_0 - func(x_0) / d_func((a + b) / 2)   # делим на df(x_0)

    if step == iter:
        return UnsolvedSolution("LimitExceeded")
    else:
        return Solution(solution=x,
                        steps=step,
                        init_approx=[(a + b) / 2],
                        abs_error=abs(x - x_0),
                        func_solve=func(x))


def transversal(a, b, eps, func, iter = 100):   # приближение методом секущих
    step = 0
    x_0 = a
    x_1 = b

    x = x_1 - (func(x_1) / (func(x_1) - func(x_0))) * (x_1 - x_0)
    while abs(x - x_1) > eps and step < iter:
        step += 1
        x_0 = x_1
        x_1 = x
        x = x_1 - (func(x_1) / (func(x_1) - func(x_0))) * (x_1 - x_0)

    if step == iter:
        return UnsolvedSolution("LimitExceeded")
    else:
        return Solution(solution=x,
                        steps=step,
                        init_approx=[a, b],
                        abs_error=abs(x - x_1),
                        func_solve=func(x))


def parse_answer(solution):
    if solution.is_found:
        print("Приближённое решение: %.12f\n"
              "Количество шагов: %d\n"
              "Начальные приближения: %s\n"
              "Последняя абс. погрешность |x_m - x_m-1|: %f\n"
              "Абсолютная величина невязки |f(x) - 0|: %.12f" % (solution.solution,
                                                              solution.steps,
                                                              str(solution.init_approx),
                                                              abs(solution.abs_error),
                                                              abs(solution.func_solve)))
    else:
        print("Превышено допустимое число итераций (%s)!" % solution.err_name)


if __name__ == '__main__':
    a = -15
    b = 5
    eps = 0.0000000001
    n = 50

    sections = root_division(a, b, func, n)

    print("Численные методы решения нелинейных уравнений\n\n"
          "Вид уравнения: 4 * cos(x) + 0.3 * x\n"
          "A = %d, B = %d, eps = %f, n = %d\n" % (a, b, eps, n))
    print("---Отделение корней (%d корней)---" % len(sections))

    for sect_num in range(len(sections)):
        print("%d) %s" % (sect_num + 1, str(sections[sect_num])))

    for sect_num in range(len(sections)):
        print("\n\n*** Отрезок %d: %s ***\n" % (sect_num+1, str(sections[sect_num])))
        a = sections[sect_num][0]
        b = sections[sect_num][1]

        print("---Метод бисекции---")
        ans = bisect(a, b, eps, func)
        parse_answer(ans)

        print("---Метод Ньютона---")
        ans = newton(a, b, eps, func, d_func)
        parse_answer(ans)

        print("---Метод Ньютона (модифицированный)---")
        ans = newton_m(a, b, eps, func, d_func)
        parse_answer(ans)

        print("---Метод секущих---")
        ans = transversal(a, b, eps, func)
        parse_answer(ans)
