import random


def remove(string):
    b = r"!@#$/.()\'&"
    for char in b:
        string = string.replace(char, "")
    string = string.replace(" ", "-")

    return string


def select_api(remaining_uses):
    li = []
    for i, remain in enumerate(remaining_uses):
        if remain > 0:
            li.append(i)
    index = random.randint(0, len(li) - 1)
    return index