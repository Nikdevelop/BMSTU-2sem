EPS = 1e-4


def convert_int(number, from_base, to_base):
    if not isinstance(number, int):
        number = int(number, from_base)
    alph = "0123456789ABCDEF"
    new_num = ""
    while number > 0:
        new_num += alph[number % to_base]
        number //= to_base

    return new_num[::-1]


def convert_float(number, from_base, to_base, prec):
    if not isinstance(number, float):
        number = __convert_float(number, from_base)
    alph = "0123456789ABCDEF"
    new_num = ""

    integer_part = int(number)
    decimal_part = number % 1

    # Conevrting int part
    while integer_part > 0:
        new_num += alph[integer_part % to_base]
        integer_part //= to_base

    new_num = new_num[::-1]
    new_num += "."

    # Converting float part
    i = 0
    while i < prec and abs(decimal_part) > EPS:
        i += 1
        decimal_part *= to_base
        new_num += alph[int(decimal_part)]

        if decimal_part >= 1:
            decimal_part %= 1

    return new_num


def __convert_float(number, from_base):
    int_part, float_part = number.split(".")
    number = int(int_part, from_base)

    for i, el in enumerate(float_part):
        number += int(el) * from_base ** (-i - 1)

    return number
