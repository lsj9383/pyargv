import pyargv

@pyargv.parse(
    pyargv.Argv("filename"),            # 不带默认参数的普通参数
    pyargv.Argv("alpha", default=13),   # 含有默认参数的普通参数
    pyargv.KeyValue("beta", "-b"),      # 不带默认参数的关键词参数
    pyargv.Boolean("debug"),            # 布尔参数(默认为False)
    )
def main(filename, alpha, beta, debug):
    print("filename:", filename)
    print("alpha:", alpha)
    print("beta:", beta)
    print("debug:", debug)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)