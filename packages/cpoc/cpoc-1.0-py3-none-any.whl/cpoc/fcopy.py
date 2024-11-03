from shutil import copy
from os.path import abspath, exists


class YourMindHasAnError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return super().__str__()


def fc(file1, file2):
    abs1 = abspath(file1)
    abs2 = abspath(file2)
    if exists(abs2) and not prompt("Do you wanna overwrite? "):
        raise YourMindHasAnError("not gonna overwrite then")
    copy(abs1, abs2)


def prompt(question: str) -> bool:
    return input(question)[0].lower() in ('y', 's')
