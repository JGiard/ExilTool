from typing import Optional

ROUTE_ATTR = '__route'
ROUTE_METHOD_ATTR = '__route_method'
NO_AUTH_ATTR = '__no_auth'


def route(path, method: Optional[str] = 'GET'):
    def decorator(f):
        setattr(f, ROUTE_ATTR, path)
        setattr(f, ROUTE_METHOD_ATTR, method)

        return f

    return decorator


def noauth(f):
    setattr(f, NO_AUTH_ATTR, True)
    return f
