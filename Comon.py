import random


def remove(string):
    b = r"!@#$/.()\'&:,;*[]{}~"
    for char in b:
        string = string.replace(char, "")
    string = string.replace(" ", "-")

    return string


def select_api(remaining_uses):
    li = []
    for i, remain in enumerate(remaining_uses):
        if remain > 0:
            li.append(i)

    if len(li) > 0:
        return random.randint(0, len(li) - 1)
    else:
        return -1


def find_0_remaining(remaining_uses):
    l0 = []
    for i, remain in enumerate(remaining_uses):
        if remain < 0 or remain == 500 or remain == 5000 or remain == 15000:
            l0.append(i)
    return l0
