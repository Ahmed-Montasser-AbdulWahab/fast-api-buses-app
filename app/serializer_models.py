from pydantic import BaseModel

class Bus(BaseModel):
    lineNumber: int
    with_slash: bool
    starting: str
    destination: str
    garage: str = "N/A"