# low-level utils

from datetime import datetime, timezone, timedelta


def modeltodict(obj, **kwargs):
    def filtered(item):
        k, v = item
        if k == '_state':
            return False
        if 'only' in kwargs:
            attrs = kwargs['only']
            if isinstance(attrs, str):
                attrs = [attrs]
            return k in attrs
        if 'exclude' in kwargs:
            attrs = kwargs['exclude']
            if isinstance(attrs, str):
                attrs = [attrs]
            return k not in attrs
        return True
    return dict(filter(filtered, vars(obj).items()))


def utcnow(**kwargs):
    dt = datetime.now(timezone.utc)
    if kwargs:
        dt += timedelta(**kwargs)
    return dt
