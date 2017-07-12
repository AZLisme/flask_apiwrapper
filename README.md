# Flask API Wrapper
[![Build Status](https://travis-ci.org/AZLisme/flask_apiwrapper.svg?branch=master)](https://travis-ci.org/AZLisme/flask_apiwrapper)[![Coverage Status](https://coveralls.io/repos/github/AZLisme/flask_apiwrapper/badge.svg?branch=master)](https://coveralls.io/github/AZLisme/flask_apiwrapper?branch=master)

[中文README](README-cn.md)

## Usage

### Parameter Extraction

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

and you try:

```shell
> curl http://localhost:5000/api/1?name=Tony&age=18
My name is Tony, and I\'m 18, younger than Bill.
```

notice that the wrapper converts the type of the argument automatically, according to the python annotation. That's a Python 3 only feature.

#### Works with URL builder

if you use flask's URL builder, it's okay to work with this wrapper:

```python
@app.route('/api/<name>')
@api_wraps()
def api(name: str, age: int):
    pass
```

Once use url build on a argument, the wrapper ignores it, and will not convert it's type any more.

#### Default Values

Default values are fully supported, just use it in annotation:

```python
@app.route('/api/')
@api_wraps()
def api(name: str, age: int = 18):
    pass
```

Notice that argument without default value is treated as required arguement, it will raise a exception if that argument is missing.

Default value can ignore type annotation.

### Response Handler

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

and you try:

```shell
> curl http://localhost:5000/api/2
{"hello": "world"}
```

and it works with correct header which make sense.

Besides dicts, you can also do this with str, list, file-like or other Iterable. Custmize handler function to support formats other than json is supported.

## Customize

Construct a new ApiWrapper instance or inherit ApiWrapper to customize behavior of wrapper.

```python
class MyWrapper(ApiWrapper):
    pass

wrapper = MyWrapper()

@wrapper.api_wraps()
def api():
    pass
```