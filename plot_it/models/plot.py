from pydantic import BaseModel
from typing import List, Optional

from plot_it.models import Chart


class Input(BaseModel):
    paths: List[str]


class Output(BaseModel):
    dir: str
    overwrite: bool


class Event(BaseModel):
    name: str
    timestamp: str
    format: str


class Plot(BaseModel):
    show_events: bool = False
    events: List[Event] = []
    input: Optional[Input]
    output: Optional[Output]
    charts: List[Chart] = []
