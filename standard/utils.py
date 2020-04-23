from .config import BAN_LIST


def filter_file(name, sub=" "):
    for b in BAN_LIST:
        name = name.replace(b, sub)
    return name
