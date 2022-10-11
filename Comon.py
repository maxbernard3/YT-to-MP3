def remove(string):
    b = r"!@#$/.()\'&"
    for char in b:
        string = string.replace(char, "")
    string = string.replace(" ", "-")

    return string
