import abc
import polars as pl


class Checks(abc.ABC):
    @abc.abstractmethod
    def determine_quality_checks(self, profiler: pl.DataFrame=None, sample: pl.DataFrame=None):
        pass