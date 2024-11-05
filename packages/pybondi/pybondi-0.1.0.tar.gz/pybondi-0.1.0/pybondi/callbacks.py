from abc import ABC, abstractmethod
from typing import Any
from typing import Sequence
from mlbus.publisher import Publisher

class Callback(ABC):
    def __init__(self):
        self.publisher = Publisher()

    def bind(self, publisher: Publisher):
        self.publisher = publisher

    @abstractmethod
    def __call__(self, *args, **kwargs): ...

    @abstractmethod
    def flush(self): ...

    @abstractmethod
    def reset(self): ...


class Callbacks:
    def __init__(self, callbacks: Sequence[Callback]):
        self.publisher = Publisher()
        self.list = list[Callback](callbacks)
    
    def set(self, name: str, value: Any) -> None:
        [setattr(callback, name, value) for callback in self.list]

    def bind(self, publisher: Publisher):
        [callback.bind(publisher) for callback in self.list]

    def __call__(self, *args, **kwargs):
        [callback(*args, **kwargs) for callback in self.list]

    def flush(self):
        [callback.flush() for callback in self.list]
        
    def reset(self):
        [callback.reset() for callback in self.list]