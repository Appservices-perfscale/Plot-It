from pydantic import BaseModel


class PlotResult(BaseModel):    
    success: int = 0
    failed: int = 0
