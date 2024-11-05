from abc import ABC
from typing import Callable
from typing import Any
from typing import Optional
from logging import getLogger
from collections import deque

logger = getLogger(__name__)

class Event(ABC):
    """
    Event is an abstract base class for domain events.
    """
    ...

class Command(ABC):
    """
    Command is a class representing a request to perform an action.
    """
    ...

class Messagebus:
    """
    Messagebus is a class that routes domain events and commands to their respective handlers.
    It maintains a queue of messages to be processed.

    Attributes:
        handlers: A dictionary mapping command types to their corresponding handlers.
        consumers: A dictionary mapping event types to a list of their consumers.
        queue: A deque storing messages to be processed.
    """

    def __init__(self):
        self.handlers = dict[type[Command], Callable[[Command], None]]()
        self.consumers = dict[type[Event], list[Callable[[Event], None]]]()
        self.queue = deque[Command | Event]()


    def handle(self, command: Command):
        """
        Handles a given command by invoking its corresponding handler.

        Parameters:
            command: The command to be handled.

        Raises:
            ValueError: If no handler is found for the command type.
        """
        handler = self.handlers.get(type(command), None)
        if not handler:
            raise ValueError(f"Command not found for message {command}")
        handler(command)


    def consume(self, event: Event):
        """
        Consumes a given event by invoking its registered consumers.

        Parameters:
            event: The event to be consumed.
        """
        for consumer in self.consumers.get(type(event), []):
            try:
                consumer(event)
            except Exception as exception:
                logger.error(f"Error while consuming event {event}")
                logger.debug(exception, exc_info=True)


    def dispatch(self, message: Event | Command) -> Optional[Any]:
        """
        Routes a message to its appropriate handler or consumer.

        Args:
            message: The message to be routed, either a domain event or a command.

        Raises:
            TypeError: If the message is neither an event nor a command.

        Returns:
            The result of the command handler, if the message is a command.
            None, otherwise.
        """
        if isinstance(message, Command):
            self.handle(message)
        elif isinstance(message, Event):
            self.consume(message)
        else:
            raise TypeError(f"The message {message} wasn't an event nor a command instance")


    def enqueue(self, message: Event | Command):
        """
        Enqueues a message to be processed later.

        Args:
            message: The message to be enqueued.
        """
        self.queue.append(message)


    def dequeue(self) -> Event | Command:
        """
        Dequeues the next message from the queue.

        Returns:
            The dequeued message.
        """
        return self.queue.popleft()
    

    def run(self):
        """
        Processes all messages in the queue until it is empty.
        """
        while self.queue:
            message = self.dequeue()
            self.dispatch(message)