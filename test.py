# test.py

import pyargv

@pyargv.parse(
    pyargv.Argv("a", default="I'm a"),
    pyargv.KeyValue("name", "-n"),
    pyargv.KeyValue("age", "-a", default="18"),
    pyargv.Boolean("debug"))
def main(a, name, age, debug):
    print("a:", a)
    print("name:", name)
    print("age:", age)
    print("debug:", debug)

if __name__ == '__main__':
    main()