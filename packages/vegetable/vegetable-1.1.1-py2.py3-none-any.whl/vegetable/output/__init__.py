from abc import ABC, abstractmethod
import os


class OutputFormatter(ABC):
    """Base class of object that formats tabular into a string form"""
    def __init__(self, record_separator):
        self.record_separator = os.linesep if record_separator is None else record_separator

    @abstractmethod
    def __call__(self, table):
        """
        Returns a string with the formatted table.
        """
        pass

    def header(self, *a, **k):
        """
        Return a string with the column names (not including a record separator).
        """
        raise RuntimeError(f"{self.__class__.__name__} does not support line-by-line output mode.")

    def separator(self, *a, **k):
        """
        Returns a string separator line if appropriate for the output format (not including a record separator).
        """
        raise RuntimeError(f"{self.__class__.__name__} does not support line-by-line output mode.")

    def mast_head(self, *a, **k):
        """
        Returns header() and separator() joined with the record separator if both values are not empty strings.
        """
        raise RuntimeError(f"{self.__class__.__name__} does not support line-by-line output mode.")

    def row(self, *a, **k):
        """
        Returns one record formatted according to the output format (not including a record separator).
        """
        raise RuntimeError(f"{self.__class__.__name__} does not support line-by-line output mode.")
