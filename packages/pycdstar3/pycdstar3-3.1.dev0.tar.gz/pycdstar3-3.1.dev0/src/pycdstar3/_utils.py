import os
import urllib.parse
from threading import Thread, Event
import time

PATH_TYPES = (str,)
if hasattr(os, "PathLike"):
    PATH_TYPES = (str, os.PathLike)  # pragma: no cover


class cached_property(object):
    def __init__(self, func):
        self.__doc__ = getattr(func, "__doc__")
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


def url_split_auth(url: str):
    """Extract and remove auth information from an URL.
    Return a (cleaned-url, username, password) tuple.

    The cleaned-url will have any auth information removed from the netloc part.
    Username and password may be None if not present.
    """
    split = urllib.parse.urlsplit(url)
    username, password = split.username, split.password
    if username or password:
        netloc = split.hostname
        if split.port:
            netloc += ":" + str(split.port)
        url = urllib.parse.urlunsplit(split._replace(netloc=netloc))
    return url, username, password


class IntervalTimer(Thread):
    """A thread that runs a function over and over until stopped.

    Example::
        t = IntervalTimer(30.0, f, args=None, kwargs=None)
        t.start()
        t.cancel()
    """

    def __init__(self, interval, function, *args, **kwargs):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()

    def set_interval(self, interval):
        self.interval = interval

    def cancel(self):
        self.finished.set()

    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def cascade_sleep(start: float, gain: float, maximum: float):
    """An iterator that sleeps an increasing amount of time between
    iterations and returns the total time spend sleeping."""
    ts = time.time()
    sleep = start
    while True:
        time.sleep(sleep)
        yield time.time() - ts
        sleep = min(maximum, sleep + gain)
