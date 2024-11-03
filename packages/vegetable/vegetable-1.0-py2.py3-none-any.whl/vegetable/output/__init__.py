from abc import ABC, abstractmethod


class TableFormatter(ABC):
    """Base class of object that formats a table into a string form"""

    @abstractmethod
    def __call__(self, table):
        pass
