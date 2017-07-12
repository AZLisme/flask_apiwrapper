# -*- encoding: utf-8 -*-


from .wrapper import ApiWrapper
from .errors import *

wrapper = ApiWrapper()

api_wraps = wrapper.wraps_api
