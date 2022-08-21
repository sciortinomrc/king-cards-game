def get_value(val):
    val = val[1:]
    if val == "J":
        return 11
    if val == "Q":
        return 12
    if val == "K":
        return 13
    if val == "A":
        return 14

    return int(val)