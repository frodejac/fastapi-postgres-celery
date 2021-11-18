from abc import ABC, abstractmethod


class ResourceNotFoundException(Exception, ABC):
    @abstractmethod
    def __str__(self):
        ...
