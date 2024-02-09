def convert(number, from_base, to_base):
    if not isinstance(number, int):
        number = int(number, from_base)
    alph = "0123456789ABCDEF"
    new_num = ""
    while number > 0:
        new_num += alph[number % to_base]
        number //= to_base

    return new_num[::-1]

