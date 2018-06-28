import pyargv


@pyargv.argvload((
    pyargv.Argv("origin"),
    pyargv.Argv("to",),
    pyargv.Argv("alpha", 13),
    pyargv.Boolean("debug"),
    ))
def main(origin, to, alpha, debug):
    print("origin:", origin)
    print("to:", to)
    print("alpha:", alpha)
    print("debug:", debug)

if __name__ == "__main__":
    main()