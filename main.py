from typing import Iterator, SupportsIndex
import os
import re
import write

FONCTION_REGEX = "(([a-z]|&|\\*|:)+\\s(&|\\*)?([a-z]+::)*([a-z]|_|operator..?)+\\(([a-z]|_|\\s|,|&|\\*|:)*\\))"

# Try and ask if user want to delete previous (if existing)
try:
    os.makedirs(os.getcwd() + "/tests")
except FileExistsError:
    value = os.system("bash " + os.path.dirname(__file__) + "/remove.sh")
    if value:
        exit(value)

# Retry if removed at previous part
try:
    os.makedirs(os.getcwd() + "/tests")
except FileExistsError:
    pass

EXCEPTIONS = [".git", "bonus", "test", "tests", "log", ".log"]

hppfilelist: list[str] = []
cppfilelist: list[str] = []

try:
    paths = [os.getcwd()]
    while not len(paths) == 0:
        actual_path = paths.pop()
        hppfilelist = hppfilelist + [os.path.join(actual_path, f) for f in os.listdir(actual_path) if
                                     os.path.isfile(os.path.join(actual_path, f)) and f.endswith(".hpp") and
                                     f not in EXCEPTIONS]
        cppfilelist = cppfilelist + [os.path.join(actual_path, f) for f in os.listdir(actual_path) if
                                     os.path.isfile(os.path.join(actual_path, f)) and f.endswith(".cpp") and
                                     f not in EXCEPTIONS]
        paths = paths + [os.path.join(actual_path, f) for f in os.listdir(actual_path) if
                         f not in EXCEPTIONS and not os.path.isfile(os.path.join(actual_path, f))]
except Exception:
    cppfilelist = []
    hppfilelist = []

Fonctions: list[tuple[str, SupportsIndex, Iterator[re.Match[str]] | list[str]]] = []

for path in cppfilelist:
    with open(path) as f:
        txt = f.readlines()
    for i in range(len(txt)):
        if len(re.findall(FONCTION_REGEX, txt[i], re.IGNORECASE)) > 0:
            Fonctions += [(path, i, re.finditer(FONCTION_REGEX, txt[i], re.IGNORECASE))]
for path in hppfilelist:
    with open(path) as f:
        txt = f.readlines()
    for i in range(len(txt)):
        if len(re.findall(FONCTION_REGEX, txt[i], re.IGNORECASE)) > 0:
            Fonctions += [(path, i, re.finditer(FONCTION_REGEX, txt[i], re.IGNORECASE))]

for i in range(len(Fonctions)):
    f = Fonctions[i]
    l: list[str] = []
    for e in f[2]:
        if not isinstance(e, str):
            elem = e.string
        else:
            elem = e
        if elem.strip().startswith("return"):
            continue
        if elem.strip().startswith("if"):
            continue
        if elem.strip().startswith("else if"):
            continue
        if elem.strip().startswith("for"):
            continue
        m = re.match("([a-z]+)::([a-z]+)", elem, re.IGNORECASE)
        if m and len(m.groups()) > 1 and m.groups()[0] == m.groups()[1]:
            continue
        l.append(elem)
    Fonctions[i] = (f[0], f[1], l)
    del f

for f in Fonctions:
    if not isinstance(f[2], list):
        raise TypeError("Cannot convert tests")
    write.write_test(f[0], f[2])
