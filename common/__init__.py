# low-level utils

def modeltodict(obj, **kwargs):
    def filtered(item):
        k, v = item
        if k == '_state':
            return False
        if 'only' in kwargs:
            return k in kwargs['only']
        if 'exclude' in kwargs:
            return k not in kwargs['exclude']
        return True
    return dict(filter(filtered, vars(obj).items()))
