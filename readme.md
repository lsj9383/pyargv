# PYARGV
这是一个轻量级的Python命令行参数加载器，通过装饰器实现对命令行参数的解析和加载，当前版本支持以下参数加载功能:
* 位置参数
* 布尔参数
* 默认参数
* 关键词参数
* 类型转换
* 自动生成帮助文档

## 一、安装
下载本仓库，并进入仓库根目录，通过以下指令安装pyargv包:
```
python setup.py install
```
安装完成后，就可以在Python中通过以下方式引入pyargv包：
```
import pyargv
```
## 二、最小示例
要使用pyargv的参数解析功能，`必须`编写一个主函数，并将主函数用于搭载一个装饰器，通过主函数的参数列表使得代码可以获取到命令行参数。
```python
# test.py

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
```

```sh
>> python test.py lena.jpg -b 4 --debug

# 命令行输出
filename: lena.jpg
alpha: 13
beta: 4
debug: True
```
仅需要注意，Boolean类型的参数，载命令行中输入的时候，需要添加两个划线。如果生成整个输入参数文档，可以通过`python test.py --help`获得。
```sh
>> python test.py --help

# 命令行输出
position argv:
  filename   default:None
  alpha   default:13
kv argv:
  --beta <val> | beta:<value>   default:None
boolean argv:
  --debug   default:False
  --help   default:False
```


## 三、使用详情
`函数参数列表`是指的在定义函数时列出需要接收哪些参数。为了接收命令行的参数，需要通过装饰器`@pyargv.parse()`指定`命令行参数列表`，再通过函数参数列表来让被装饰的函数接收来自命令汗的参数，类似如下接收方式:
```python
@pyargv.parse(arg1, arg2, ...)
def main(arg1, arg2, ...):
    ...
```
pyargv.parse()装饰器提供了以下4种命令行参数接收方案。
### 1.*位置参数*
根据命令行参数列表的位置来接收参数，位置参数在命令行参数列表中通过`pyargv.Argv`对象进行表示:
```python
# test.py

import pyargv

@pyargv.parse(
    pyargv.Argv("a"),
    pyargv.Argv("b"))
def main(a, b):
    print("a:", a)
    print("b:", b)

if __name__ == '__main__':
    main()
```
通过如下命令行进行调用，并可以得到程序的输出:
```sh
>> python test.py 1 2

# 命令行输出
a: 1
b: 2
```
若缺失参数，程序则会抛出异常:
```
>> python test.py 1

Traceback (most recent call last):
  File "test.py", line 11, in <module>
    main()
  File "/Users/lushuaiji/Documents/design/python/pyargv/pyargv/__init__.py", line 149, in inner
    __kwsload__(kws, norm_argvlist, bool_argvlist, kv_argvlist)
  File "/Users/lushuaiji/Documents/design/python/pyargv/pyargv/__init__.py", line 112, in __kwsload__
    __verify_missing_argv__(kws)
  File "/Users/lushuaiji/Documents/design/python/pyargv/pyargv/__init__.py", line 93, in __verify_missing_argv__
    raise Exception(__argv_cache__[k].ed)
Exception: missing 1 required argument:'b'
```
这个异常是在被装饰函数进行调用时抛出的，因此较好的处理方式是对该函数的调用进行捕获异常和异常处理:
```python
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
```
### 2.*默认参数*
在通过命令行传参，但是参数列表中的参数缺失时会抛出异常。可以通过指定参数的默认值，在命令行传参时若没有提供该位置参数，则采用默认值，若提供则采用提供的值。(默认值不局限于位置参数，布尔参数和关键词参数都可以提供默认值)。在参数列表的参数对象初始化时，指定default参数即可。
```python
# test.py

import pyargv

@pyargv.parse(
    pyargv.Argv("a", default="I'm a"),
    pyargv.Argv("b", default="I'm b"))
def main(a, b):
    print("a:", a)
    print("b:", b)

if __name__ == '__main__':
    main()
```

```sh
>> python3 test.py

# 命令行输出
a: I'm a
b: I'm b
```
需要注意，`None`不能作为默认参数，若设置`default=None`，默认参数设置将会无效。
### 3.*布尔参数*
对于一些开关型参数的表示，若是仅仅通过位置参数来传True或者False，命令行传参的可读性将会特别差。例如程序通过布尔变量表示开启调试模式、开启日志记录、关闭邮件发放，则可能的命令行调用方式将会是`python programe.py True True False`，这看起来非常难受。`pyargv`所提供的布尔参数非常适合于此类开关函数，通过直接写出需要打开的开关即可:
```
>> python programe.py --debug --log
```
布尔参数在参数列表中通过`pyargv.Boolean`进行指明:
```python
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
```
命令行中通过`--<key>`的形式，来声明该参数为True，否则为False:
```sh
>> python test.py 1 --debug --log

# 命令行输出
a: 1
b: I'm b
debug: True
log: True
email: False
```
另外，需要注意的时，布尔参数不受位置限制。这意味着在命令行参数列表中布尔参数可以写在任何位置，在命令行传参中也可以在任何位置写布尔参数。
### 4.*关键词参数*
对于命令行传参，参数数量较多时，会非常影响可读性，也容易忘记哪个位置对应的是哪个参数。关键词参数传参在命令行中有两种表现形式:
```
>> python programe.py key:value
>> python programe.py -key value
```
以上两种形式都能把value值传递给被修饰函数的名字为key的变量。关键词参数在参数列表中通过`pyargv.KeyValue`进行声明:
```python
# test.py

import pyargv

@pyargv.parse(
    pyargv.Argv("a", default="I'm a"),
    pyargv.KeyValue("name", "-n"),
    pyargv.KeyValue("age", "-a", default="18"),
    pyargv.Boolean("debug"))
def main(a, name, age, debug):
    print("a:", a)
    print("name", name)
    print("age", age)
    print("debug:", debug)

if __name__ == '__main__':
    main()
```
关键词参数也可以通过default来设置默认值，对于不带默认值的关键词参数若在传参时没有给出参数，同样会抛出异常。在进行关键词参数传参时，其位置是任意的。
```sh
>> python3 test.py -n hello
>> python3 test.py name:hello   # 和上一行等价

# 命令行输出
a: I'm a
name: hello
age: 18
debug: False
```
### 5.*类型转换*
命令行参数输入的全是字符串，为了更好的应用这些参数，pyargv提供了类型转换的功能，可以将对应的字符串转换为对应的类型。位置参数和关键词参数都可以通过提供valtype来设置该参数的类型，在没有设置时valtype默认为`str`:
```python
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
```
在命令行传参后，pyargv会将参数字符串转换为其valtype所指定的类型，再交给被修饰的函数。
```sh
>> python test.py 1.3 -n hello

# 命令行输出
alpha: 1.3 <class 'float'>
name: hello <class 'str'>
age: 18 <class 'int'>
debug: False <class 'bool'>
```
