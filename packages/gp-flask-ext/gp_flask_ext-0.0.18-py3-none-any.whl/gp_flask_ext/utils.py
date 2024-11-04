import time
import threading
from decorator import decorator

_KEYS_LAST_CALL = {}
_KEYS_TIMEER = {}
_KEYS_INTERVAL = {}

def debounce_info():
    now = time.time()
    ret = []
    for key, value in _KEYS_LAST_CALL.items():
        item = {
            "key": key,
            "last_call": value,
            "interval": _KEYS_INTERVAL[key],
            "elapsed": now - value,
            "remaining": _KEYS_INTERVAL[key] - (now - value),
        }
        ret.append(item)
    return ret

def debounce(interval=1, key_fun=None):
    """避免函数被频繁调用"""
    @decorator
    def _debounce(func, *args, **kwargs):
        if key_fun:
            _key = key_fun(args, kwargs)
        else:
            _key = func.__name__
        now = time.time()
        last_time = _KEYS_LAST_CALL.get(_key, 0)
        _KEYS_INTERVAL[_key] = interval
        if now - last_time > interval:
            _KEYS_LAST_CALL[_key] = now
            return func(*args, **kwargs)
        else:
            _timer = _KEYS_TIMEER.get(_key)
            if _timer:
                _timer.cancel()
            _timer = threading.Timer(interval, func, args, kwargs)
            _KEYS_TIMEER[_key] = _timer
    return _debounce