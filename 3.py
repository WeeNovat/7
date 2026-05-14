import functools, time

def cache(max_size=128):
    def decorator(func):
        _cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            if args in _cache: return _cache[args]
            res = func(*args)
            if len(_cache) >= max_size: _cache.pop(next(iter(_cache)))
            _cache[args] = res
            return res
        return wrapper
    return decorator

def log(level="INFO"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            print(f"[{level}] Виклик {func.__name__}")
            try:
                res = func(*args, **kwargs)
                print(f"[{level}] {func.__name__} -> {res} ({time.perf_counter()-start:.4f}s)")
                return res
            except Exception as e:
                print(f"[ERROR] {func.__name__}: {e}"); raise
        return wrapper
    return decorator

@cache()
@log(level="DEBUG")
def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)

def main(): print(f"Фібоначчі(10): {fib(10)}")
if __name__ == "__main__": main()
