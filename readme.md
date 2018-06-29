# PYARGV
这是一个轻量级的Python命令行参数加载器，通过装饰器实现对命令行参数的解析和加载，当前版本支持以下参数加载功能:
* 位置参数
* 布尔参数
* 默认参数
* 关键词参数
* 自动生成帮助文档(*待续*)

## 一、安装
下载本仓库，并进入仓库根目录，通过以下指令安装pyargv包:
```
python setup.py install
```
安装完成后，就可以在Python中通过以下方式引入pyargv包：
```
import pyargv
...
```

## 二、最小示例
要使用pyargv的参数解析功能，`必须`编写一个主函数，并将主函数用于搭载一个装饰器，通过主函数的参数列表使得代码可以获取到命令行参数。
```python
# test.py

import pyargv

@pyargv.parse(
    pyargv.Argv("filename"),            # 不带默认参数的普通参数
    pyargv.Argv("alpha", 13),           # 含有默认参数的普通参数
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
在命令行中输入`python test.py lena.jpg -b 4 --debug`, 则在命令行中将会返回：
```
filename: lena.jpg
alpha: 13
beta: 4
debug: True
```
仅需要注意，Boolean类型的参数，载命令行中输入的时候，需要添加两个划线。

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
    pyargv.pyargv.Argv("a"), 
    pyargv.pyargv.Argv("b"))
def main(a, b):
    print("a:", a)
    print("b:", b)

if __name__ == '__main__':
    main()
```
通过如下命令行进行调用，并可以得到程序的输出:
```
>> python test.py 1 2

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
### 2.*默认参数*
### 3.*布尔参数*
### 4.*关键词参数*
