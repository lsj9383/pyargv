# test.py

import pyargv

@pyargv.parse(
    pyargv.Argv("a", default="I'm a"), 
    pyargv.Argv("b", default="I'm b"),
    pyargv.Boolean("debug"),
    pyargv.Boolean("log"),
    pyargv.Boolean("email"))
def main(a, b, debug, log, email):
    print("a:", a)
    print("b:", b)
    print("debug:", debug)
    print("log:", log)
    print("email:", email)

if __name__ == '__main__':
    main()