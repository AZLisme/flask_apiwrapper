# -*- encoding: utf-8 -*-

import os
import random
import tempfile
import unittest

import flask
import pytest

from flask_apiwrapper import ParameterTypeNotMatchException, api_wraps

app = flask.Flask('TestApplication')

ALL_METHODS = ['GET', 'POST', 'PUT', 'DELETE']


def run_with_all_methods(url, verify_func):
    with app.test_client() as c:
        for rv in [f(url) for f in (c.get, c.post, c.put, c.delete)]:
            verify_func(rv)


@app.route('/test1/normal', methods=ALL_METHODS)
@api_wraps()
def api_1_normal():
    return 'ok'


@app.route('/test2/args/<name>', methods=ALL_METHODS)
@api_wraps('name')
def api_2_with_args(name, arg1):
    return '%s and %s' % (name, arg1)


@app.route('/test3/type', methods=ALL_METHODS)
@api_wraps()
def api_3_type(arg_int: int, arg_str: str, arg_bool: bool):
    if isinstance(arg_int, int) and isinstance(arg_str, str) and isinstance(arg_bool, bool):
        return 'ok'
    else:
        return 'wrong', 400


@app.route('/test3/type_force', methods=ALL_METHODS)
@api_wraps(force_match=True)
def api_3_type_force(arg_int: int, arg_str: str, arg_bool: bool):
    if isinstance(arg_int, int) and isinstance(arg_str, str) and isinstance(arg_bool, bool):
        return 'ok'
    else:
        return 'wrong', 400


def test_1_normal_use():
    def verify(rv):
        assert rv.status_code == 200
        assert rv.data == b'ok'
    run_with_all_methods('/test1/normal', verify)


def test_2_with_args():
    name = random.randint(1, 100)
    arg1 = random.randint(1, 1000)

    def verify_ok(rv):
        assert rv.status_code == 200
        assert rv.data.decode('ascii') == "%s and %s" % (name, arg1)

    run_with_all_methods('/test2/args/%s?arg1=%s' % (name, arg1), verify_ok)
    run_with_all_methods('/test2/args/%s?arg1=%s&arg2=hello' %
                         (name, arg1), verify_ok)

    def verify_404(rv):
        assert rv.status_code == 404

    run_with_all_methods('/test2/args/', verify_404)


def test_3_type():
    with app.test_client() as c:
        rv = c.get('/test3/type?arg_int=1&arg_str=helloworld&arg_bool=True')
        assert rv.status_code == 200

    with app.test_client() as c:
        rv = c.get('/test3/type?arg_int=good&arg_str=helloworld&arg_bool=True')
        assert rv.status_code == 200

    with app.test_client() as c:
        rv = c.get('/test3/type_force?arg_int=1&arg_str=helloworld&arg_bool=True')
        assert rv.status_code == 200

    with app.test_client() as c:
        with pytest.raises(ParameterTypeNotMatchException):
            rv = c.get(
                '/test3/type_force?arg_int=good&arg_str=helloworld&arg_bool=True')
