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
    if not all((prompt("Do you really want to copy that file? "), prompt("Do you realize that if you copy that file you won't get any money? "), prompt("Do you realize that if you copy that file your PC will find out?"))): # noqa
        raise YourMindHasAnError("ok, not gonna copy")
    if exists(abs2) and not prompt("Do you wanna overwrite? "):
        raise YourMindHasAnError("not gonna overwrite then")
    copy(abs1, abs2)


def prompt(question: str) -> bool:
    return input(question)[0].lower() in ('y', 's')
