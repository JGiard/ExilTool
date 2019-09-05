from inspect import signature
from typing import Optional

ROUTE_ATTR = '__route'
ROUTE_METHOD_ATTR = '__route_method'
ROUTE_DATA_TYPE_ATTR = '__route_data_type'


def route(path, method: Optional[str] = 'GET'):
    def decorator(f):
        setattr(f, ROUTE_ATTR, path)
        setattr(f, ROUTE_METHOD_ATTR, method)
        for name, param in signature(f).parameters.items():
            if name == 'data':
                setattr(f, ROUTE_DATA_TYPE_ATTR, param.annotation)

        return f

    return decorator
