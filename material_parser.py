import re


def get_expression(string=""):

    regex = re.compile(r"^Expressions\(\d\)=([a-z]*)", re.I)
    expression = regex.findall(string.strip())
    return expression[0] if expression else 0


