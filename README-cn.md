# Flask API Wrapper

[![Build Status](https://travis-ci.org/AZLisme/flask_apiwrapper.svg?branch=master)](https://travis-ci.org/AZLisme/flask_apiwrapper)[![Coverage Status](https://coveralls.io/repos/github/AZLisme/flask_apiwrapper/badge.svg?branch=master)](https://coveralls.io/github/AZLisme/flask_apiwrapper?branch=master)

[中文README](README-cn.md)

## 使用方法

### 提取参数

```python
import flask
from flask_apiwrapper import api_wraps

app = flask.Flask('demo')

@app.route('/api/1')
@api_wraps()
def api_1(name: str, age: int):
    bill = 20
    return "My name is %s, and I'm %d, %s Bill." % (
        name, age, 'older than' if age > bill else "younger than" if age < bill else "same with" 
    )

app.run('localhost', 5000)
```

然后在终端中尝试:

```shell
> curl http://localhost:5000/api/1?name=Tony&age=18
My name is Tony, and I\'m 18, younger than Bill.
```

所有的参数都会按照Python的类型注解自动转换，当然这需要Python3的支持。

#### 兼容Flask构造器

如果你想使用Flask的URL构造器，ApiWrapper完全兼容：

```python
@app.route('/api/<name>')
@api_wraps()
def api(name: str, age: int):
    pass
```

一旦使用URL构造器，那么该参数将被忽略，不再保证类型注解的准确性。

#### 参数默认值

完全支持函数参数默认，直接在注解中使用即可：

```python
@app.route('/api/')
@api_wraps()
def api(name: str, age: int = 18):
    pass
```

请注意，不带默认值的参数将被视为必须参数，如果缺失则会抛出一个错误。如果需要一个可选参数，可以指定其默认值为None。

默认值可以无视类型转换。

### 处理响应值

```python
import flask
from flask_apiwrapper import api_wraps

app = flask.Flask('demo')


@app.route('/api/2')
@api_wraps()
def api_2():
    return dict(hello='world')

app.run('localhost', 5000)
```

然后在终端中尝试:

```shell
> curl http://localhost:5000/api/2
{"hello": "world"}
```

所有的响应类型都会自动设置好正确的Header以保证兼容性。

除了Dict外，返回值还支持str, list, file-like, 以及其他Iterable。也可以自定义处理函数，返回Json以外的格式

## 自定义

要自定义Wrapper的行为，你可以：

+ 用自己的参数实例化一个ApiWrapper
+ 继承ApiWrapper或者BaseWrapper添加自己行为，如以下示范：

```python
class MyWrapper(ApiWrapper):
    pass

wrapper = MyWrapper()

@wrapper.api_wraps()
def api():
    pass
```