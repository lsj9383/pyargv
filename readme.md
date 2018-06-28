# PYARGV
这是一个轻量级的Python命令行参数加载器，通过装饰器实现对命令行参数的解析和加载，当前版本支持以下参数加载功能:
* 参数列表
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

@pyargv.parse((
    pyargv.Argv("filename"),            # 不带默认参数的普通参数
    pyargv.Argv("alpha", 13),           # 含有默认参数的普通参数
    pyargv.KeyValue("beta", "-b"),      # 关键词参数
    pyargv.Boolean("debug"),            # 布尔参数
    ))
def main(filename, alpha, beta, debug):
    print("filename:", filename)
    print("alpha:", alpha)
    print("beta:", beta)
    print("debug:", debug)

if __name__ == '__main__':
    main()
```
在命令行中输入`python test.py lena.jpg -b 4 --debug`, 则在命令行中将会返回：
```
filename: lena.jpg
alpha: 13
beta: 4
debug: True
```

## 三、使用详情
### 1.*参数列表*
### 2.*布尔参数*
### 3.*默认参数*
### 4.*关键词参数*
