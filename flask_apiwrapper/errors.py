# -*- encoding: utf-8 -*-


class ApiException(BaseException):
    pass


class ApiRuntimeException(ApiException):
    pass


class ApiError(ApiException):
    pass


class ApiReturnValueError(ApiError):
    pass


class ParameterNotFoundException(ApiRuntimeException):
    pass


class ParameterTypeNotMatchException(ApiRuntimeException):
    pass
