# Flask API Wrapper

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
@api_wraps("name")
def api(name: str, age: int):
    pass
```

`api_wraps` 函数接受一个可选参数，指明给上层的flask路由暴露哪些参数。这些参数会被wrapper忽略。

你可以用空格分割的字符串或者一个参数列表来指定，以下两个例子完全等价：

+ "name age gender"
+ ["name", "age", "gender"]

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