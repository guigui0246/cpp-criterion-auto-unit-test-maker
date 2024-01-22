from os import PathLike
import os, datetime

with open(os.path.dirname(__file__) + "/OWNER.txt") as f:
    OWNER = f.readlines()[0].removesuffix("\n")

def make_test_file(name:PathLike) -> None:
    file = os.path.join(os.path.dirname(name), "tests/test_"+os.path.basename(name)+".cpp")
    if not os.path.isfile(file) and os.access(file, 0):
        raise FileNotFoundError("A non file \"" + file + "\" was found")
    if os.access(file, 511):
        return
    with open(file, "w") as f:
        f.write("""/*
** """+OWNER+""" PROJECT, """+str(datetime.date.today().year)+"""
** """+os.path.basename(os.getcwd())+"""
** File description:
** Auto-unit-test
*/

#include <criterion/criterion.h>
#include \""""+os.path.basename(name)+""".hpp\"
""")

def write_test(name:PathLike, fonctions:list[str]):
    name = str(name).removesuffix(".hpp").removesuffix(".cpp")
    file = os.path.join(os.path.dirname(name), "tests/test_"+os.path.basename(name)+".cpp")
    make_test_file(name)
    with open(file, "a") as f:
        try:
            f.write(f"""\nTest({os.path.dirname(name)}, {fonctions[0].split()[1].split("::")[-1].removeprefix("&").removeprefix("*")})\n""")
            f.write("{\n")
            f.writelines(fonctions)
            f.write("}\n\n")
        except IndexError:
            pass
