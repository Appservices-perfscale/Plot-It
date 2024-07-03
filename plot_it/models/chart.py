from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from plot_it.models import Axis

class ChartType(str, Enum):
    timeseries = "timeseries"

class Chart(BaseModel):
    type: ChartType
    name: str
    show_events: bool = True
    data: List[str]
    xaxis: Optional[Axis] = Axis()
    yaxis: Axis
