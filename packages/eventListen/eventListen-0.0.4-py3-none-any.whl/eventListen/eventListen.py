from typing import Any, Callable
from proto import proto
from copy import copy

with proto("Events") as Events:
    @Events
    def new(self):
        self.obj = {}
        self.events = []
        return
    
    @Events
    def observe(self, callback: Callable[[], Any]) -> Callable[[], Any]:
        self.events.append({"name": callback.__name__, "callback": callback})
        return callback

    @Events
    def trigger(self, event: str, *args, **kwargs) -> Any:
        for obj in copy(self.obj):
            if not obj in self.obj: return
            o = self.obj[obj]
            for e in o:
                if event == e.__name__:
                    e(*args, **kwargs)
        for e in self.events:
            if e["name"] == event:
                e["callback"](*args, **kwargs)
        return 

    @Events
    def group(self, obj: object, events: list):
        self.obj[obj] = events
        return

    @Events
    def stopObserving(self, obj: object):
        del self.obj[obj]
        return

