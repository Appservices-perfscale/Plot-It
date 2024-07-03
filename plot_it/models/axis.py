from pydantic import BaseModel
from typing import List, Optional

class Axis(BaseModel):
    name: Optional[str] = None
    formatter: Optional[str] = None
    data: Optional[str] = None
