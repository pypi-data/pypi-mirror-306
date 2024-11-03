from typing import Any, Callable
from proto import proto

with proto("Events") as Events:
    @Events
    def new(self):
        self.obj = {}
        self.events = {}
        return
    
    @Events
    def observe(self, callback: Callable[[], Any]) -> Callable[[], Any]:
        self.events[callback.__name__] = callback
        return callback

    @Events
    def trigger(self, event: str, *args, **kwargs) -> Any:
        for obj in self.obj:
            o = self.obj[obj]
            for e in o:
                if event == e.__name__:
                    e(*args, **kwargs)
        if event in self.events:
            self.events[event](*args, **kwargs)
        return 

    @Events
    def group(self, obj: object, events: list):
        self.obj[obj] = events
        return

    @Events
    def stopObserving(self, obj: object):
        del self.obj[obj]
        return

