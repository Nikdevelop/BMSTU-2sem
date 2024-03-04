# Выполнил Жижин Никита. Группа ИУ7-21Б.
# Вариант 1
# Метод половинного деления (дихотомия)

import matplotlib.pyplot as plt
import numpy as np
import math
import utils
from collections import namedtuple

ERR_OK = 0
ERR_MAX_ITER = 1

FUNC = lambda x: math.sin(x)

Solution = namedtuple("Solution", ["interval", "x", "func", "iter_count", "err_code"])


def solve_dichotomy(
    func, a: float, b: float, h: float, nmax: int, eps: float
) -> list[Solution]:

    solutions = []
    for i in range(math.ceil((b - a) / h)):
        cur_a = a + h * i
        cur_b = cur_a + h

        cur_iter = 0
        while cur_iter < nmax:
            cur_iter += 1
            c = (cur_a + cur_b) / 2
            if abs(func(c)) < eps:
                solutions.append(
                    Solution((a + h * i, a + h * (i + 1)), c, func(c), cur_iter, ERR_OK)
                )
                break
            elif func(cur_a) * func(c) < 0:
                cur_b = c
            else:
                cur_a = c
        # else:
        #     solutions.append(
        #         Solution((a + h * i, a + h * (i + 1)), c, func(c), cur_iter, ERR_MAX_ITER)
        #     )

    return solutions


def print_table(solutions: list[Solution]):
    rows = [
        [i, s.interval[0], s.interval[1], s.x, s.func, s.iter_count, s.err_code]
        for i, s in enumerate(solutions, start=1)
    ]
    utils.pprint_table(
        [
            "# solution",
            "int start",
            "int end",
            "x'",
            "f(x')",
            "iter count",
            "error code",
        ],
        rows,
    )


def find_extremums(x_axis: list, y_axis: list) -> list:
    extremums = []
    for i in range(1, len(x_axis) - 1):
        if y_axis[i - 1] < y_axis[i] and y_axis[i] > y_axis[i + 1]:
            extremums.append((x_axis[i], y_axis[i]))
        elif y_axis[i - 1] > y_axis[i] and y_axis[i] < y_axis[i + 1]:
            extremums.append((x_axis[i], y_axis[i]))

    return extremums


def find_inflection_points(x_axis: list, y_axis: list) -> list:
    inflection_points = []
    for i in range(2, len(y_axis) - 2):
        if (y_axis[i] - 2 * y_axis[i - 1] + y_axis[i - 2]) * (
            y_axis[i] - 2 * y_axis[i + 1] + y_axis[i + 2]
        ) < 0:  # Проверяем условие точки перегиба
            inflection_points.append((x_axis[i], y_axis[i]))

    return inflection_points


def main():
    a, b = utils.safe_multiple_input(">>> Input a, b: ", float, 2)
    h = utils.safe_num_input(">>> Input h: ", float)
    nmax = utils.safe_num_input(">>> Input Nmax: ", float)
    eps = utils.safe_num_input(">>> Input eps: ", float)

    if a >= b:
        print("Incorrect interval!")
        return 1

    print("Solution table:\n")
    table = solve_dichotomy(FUNC, a, b, h, nmax, eps)
    print_table(table)

    x_axis = np.arange(a, b + h, h)
    y_axis = np.array(list(map(FUNC, x_axis)), dtype=float)

    extremums = find_extremums(x_axis, y_axis)
    inflections = find_inflection_points(x_axis, y_axis)

    plt.plot(x_axis, y_axis, label = "Function plot")
    plt.xlabel("x")
    plt.ylabel("f(x)")

    plt.scatter(*zip(*extremums), color='red', label='Extremum')
    plt.scatter(*zip(*inflections), color='green', label='Inflection point')
    plt.scatter(*zip(*[[el.x, el.func] for el in table]), color='blue', label='Solution')

    plt.grid(True)
    plt.legend()
    
    plt.show()


if __name__ == "__main__":
    main()
