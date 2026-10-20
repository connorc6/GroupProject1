from abc import ABC, abstractmethod

class RequestList(ABC):
    """Part 6. Interface. Methods return results; they never print."""

    @abstractmethod
    def push(self, request): """Insert at the beginning."""

    @abstractmethod
    def append(self, request): """Insert at the end."""

    @abstractmethod
    def count(self): """Return the number of stored requests."""

    @abstractmethod
    def getAt(self, index): """Return the request at a valid position."""

    @abstractmethod
    def insertAt(self, index, request): """Insert before the current item at that position."""

    @abstractmethod
    def removeAt(self, index): """Remove and return the request at that position."""

    @abstractmethod
    def findById(self, request_id): """Return the request with this ID, or None."""

    @abstractmethod
    def __str__(self): """Return a readable representation."""

    def __len__(self):
        return self.count()
