from functools import wraps

from fastapi import Body, Request


def wrap_response(func):
    @wraps(func)
    def inner(*args, **kwargs):
        items, code, msg = func(*args, **kwargs)
        return {'result': items, 'code': code, 'msg': msg}

    return inner


def wrap_get_list_response(func):
    @wraps(func)
    def inner(*args, **kwargs):
        items, count, code, msg = func(*args, **kwargs)
        return {'result': items, 'count': count, 'code': code, 'msg': msg}

    return inner


def wrap_authorization(func):
    @wraps(func)
    def inner(*args, req: Request, **kwargs):
        # print('-----------',  req.headers.keys(), args, kwargs)
        # print('---------------', kwargs['user'].gmail)
        result, code, msg = func(*args, req, **kwargs)
        return result, code, msg

    return inner
