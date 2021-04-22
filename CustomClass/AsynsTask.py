from threading import Thread


def a_sync(func):
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    wrapper.__name__ = func.__name__

    return wrapper
