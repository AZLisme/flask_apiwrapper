# -*- encoding: utf-8 -*-

import inspect
import json
from functools import wraps
from typing import Iterable, io

import flask

from .errors import ParameterNotFoundException, ParameterTypeNotMatchException


class BaseAPIWrapper():

    @classmethod
    def dict_handler(cls, api_func, value):
        load = json.dumps(value)
        return load, 200, {'Content-Type': 'application/json'}

    @classmethod
    def iter_handler(cls, api_func, value):
        load = json.dumps(value)
        return load, 200, {'Content-Type': 'application/json'}

    @classmethod
    def str_handler(cls, api_func, value):
        return value, 200, {'Content-Type': 'text/plain'}

    @classmethod
    def fp_handler(cls, api_func, value):
        flask.send_file(value)

    @classmethod
    def default_handler(cls, api_func, value):
        raise ApiReturnValueError()

    @classmethod
    def handle_return(cls, api_func, value):
        try:
            if isinstance(value, str):
                return cls.str_handler(api_func, value)
            elif isinstance(value, dict):
                return cls.dict_handler(api_func, value)
            elif isinstance(value, Iterable):
                return cls.iter_handler(api_func, value)
            elif isinstance(value, io):
                return cls.fp_handler(api_func, value)
            elif isinstance(value, flask.Response):
                return value
            else:
                return cls.default_handler(api_func, value)
        except Exception as e:
            raise ApiReturnValueError(str(e))

    @staticmethod
    def _fetch_function_defaults_dict(func):
        spec = inspect.getfullargspec(func)
        if spec.defaults:
            return dict(zip(spec.args[-len(spec.defaults):], spec.defaults))
        else:
            return dict()

    @classmethod
    def lookup_values(cls, para_list, annotations=dict(), default_map=dict(), force_match=False):
        raise NotImplemented()

    def wraps_api(self, exposed_args=None, force_match=False):
        """wrappers a api view. 

        :param exposed_args: defines what parameters shall be exposed to flask, not handled by the wrapper.
        :param force_match: if set to True, raises `ParameterTypeNotMatchException` if fail to convert type.
        """
        def decorator(api_func):
            api_func_argset = set(api_func.__code__.co_varnames[
                                  0:api_func.__code__.co_argcount])
            api_func_annotations = api_func.__annotations__
            api_func_default_map = self._fetch_function_defaults_dict(api_func)

            request_para_set = set(api_func_argset)
            if exposed_args:
                if isinstance(exposed_args, str):
                    exposed_para_set = set(exposed_args.split(' '))
                else:
                    exposed_para_set = set(exposed_args)
                request_para_set = request_para_set - exposed_para_set

            @wraps(api_func)
            def wrapper(**kwargs):
                para_args = self.lookup_values(
                    list(request_para_set), api_func_annotations, api_func_default_map, force_match)
                if para_args and isinstance(para_args, dict):
                    kwargs.update(para_args)
                return self.handle_return(api_func, api_func(**kwargs))
            return wrapper
        return decorator


class ApiWrapper(BaseAPIWrapper):

    @classmethod
    def lookup_values(cls, para_list, annotations=dict(), default_map=dict(), force_match=False):
        result = dict()
        for para_name in para_list:
            value = flask.request.args.get(para_name)
            if value and (para_name in annotations):
                try:
                    value = annotations[para_name](value)
                except (TypeError, ValueError):
                    if force_match:
                        raise ParameterTypeNotMatchException()

            if not value:
                if para_name in default_map:
                    value = default_map[para_name]
                else:
                    raise ParameterNotFoundException()

            result[para_name] = value
        return result
