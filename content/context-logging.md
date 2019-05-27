Title: Logging with context in Python
Date: 2019-05-27 15:00:00

I love Python dearly, but its logging is… honestly, kind of a mess. The particular thing that's been bothering me lately is making the logs easy to analyze mechanically (say, with an aggregator like LogStash or Loggly or SumoLogic or whatever). Python's logging is set up to do simple context-free plaintext, which is fine for simple things, but quickly becomes a pain. The first step to simplifying this is outputting logs in a JSON format, so that things like timestamps are already split out for you. This should be something which should be in the standard library, but isn't. In fact, the standard library is set up in a way which makes doing that more complicated than it should be. But that's not what this post is about, so I'm not going to cover it here.

The second step is to include metadata in those JSON logs. It is very useful to be able to associate a given log line with a specific user or request. Passing this metadata every time gets repetitive quickly, so the standard library includes a [`LoggerAdapter` class](https://docs.python.org/3/library/logging.html#loggeradapter-objects), to which you can add the metadata, and it will automatically include it on further calls. However, this then means you have to pass this object around to anywhere you're logging, which again gets repetitive quickly. If your application is single-threaded and synchronous (as many Python applications are), you can set the adapter as a global, log on that global, and re-set it on every new request. But what do you do on a multi-threaded (or, with `asyncio`, single-threaded-but-asynchronous) application?

Enter thread-local variables. These are global within the current thread, so they can be set at the beginning of your thread, without stepping on other threads/contexts. In Python 3.7, there's also a new [`contextvars` library](https://docs.python.org/3/library/contextvars.html), which provides a simmilar concept, but aimed toward asynchronous single-threaded code. (The module documentation and [PEP-567](https://www.python.org/dev/peps/pep-0567) go into more detail on what exactly defines a "context" and how they work.) Thus, you can stick that `LoggerAdapter` in a `ContextVar` or `threading.local`, and use it to carry your logging context. 

It would be a little annoying to have to do a `.get()` on every logging call, but that's easily fixed with a quick wrapper. Below is a quick example, using `ContextVar` and [`tornado`](https://tornadoweb.org) (a web framework based on `asyncio`) in Python 3.7. (It should be noted that, since Tornado is single-threaded, this example would not work with thread-local, or without the `async def` on `get`) You can run this and curl `localhost:8888` to try it out.

```
#!/usr/bin/env python3
import json
import logging
import contextvars

import tornado.ioloop
import tornado.web

_logger_storage = contextvars.ContextVar('logger')


class ContextLogger:
    def set_logger(self, logger):
        _logger_storage.set(logger)

    def __getattr__(self, name):
        return getattr(_logger_storage.get(), name)

logger = ContextLogger()


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        logger.warning('hi')
        self.write("Hello, world")

    def prepare(self):
        adapter = logging.LoggerAdapter(logging.getLogger('http'), {})
        adapter.extra['user-agent'] = self.request.headers.get('User-Agent')
        logger.set_logger(adapter)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # A JSON format for everything would be better in reality, but for
    # simplicity I've used a separate handler with a simple format on it.
    formatted_handler = logging.StreamHandler()
    formatted_handler.setFormatter(logging.Formatter('%(user-agent)s %(msg)s'))
    logging.getLogger('http').addHandler(formatted_handler)
    app = tornado.web.Application([
        (r"/", MainHandler),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
```
