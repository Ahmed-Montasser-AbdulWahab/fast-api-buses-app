from pydantic import BaseModel

class MicroBus(BaseModel):
    id: int
    starting: str
    destination: str