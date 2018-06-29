# test.py

import pyargv

@pyargv.parse(
    pyargv.Argv("alpha", valtype=float),
    pyargv.KeyValue("name", "-n"),
    pyargv.KeyValue("age", "-a", default="18", valtype=int),
    pyargv.Boolean("debug"),
    )
def main(alpha, name, age, debug):
    print("alpha:", alpha, type(alpha))
    print("name:", name, type(name))
    print("age:", age, type(age))
    print("debug:", debug, type(debug))

if __name__ == '__main__':
    main()