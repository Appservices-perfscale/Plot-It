from abc import ABC, abstractmethod
from plot_it.models import Plot, Chart


class InvalidChartType(ValueError):
    pass


class Engine(ABC):
    @abstractmethod
    def __init__(self, plot: Plot, data_sources: dict):
        pass

    @abstractmethod
    def __call__(self, chart: Chart):
        pass

    @abstractmethod
    def timeseries(self, chart: Chart):
        pass
