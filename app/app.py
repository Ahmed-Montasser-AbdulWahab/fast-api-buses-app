from fastapi import FastAPI, Response, status, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from db_models import Bus, Base
from serializer_models import Bus as BusSerializer

def init_db():
    db = SessionLocal()
    try:
        db_buses = [
                Bus(
                    lineNumber=1001,
                    with_slash=False,
                    starting="First Settlement",
                    destination="Tahrir",
                    garage="Nasr"
                ),
                Bus(
                    lineNumber=1002,
                    with_slash=False,
                    starting="Matbaa",
                    destination="Masakn Ain Shams",
                    garage="Gesr Suez"
                )
                ]
        db_buses_count = db.query(Bus).count()

        if db_buses_count != 0:
            return
        
        for bus in db_buses:
            db.add(bus)
            db.commit()
    finally:
        db.close()

# Create tables in the database
Base.metadata.create_all(bind=engine)

init_db()

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")



# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/", status_code=status.HTTP_200_OK)
def home_page():
    return {"message": "This is the Home Page"}

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"message": "Service is healthy"}

@app.post("/buses/", status_code=status.HTTP_201_CREATED)
def create_bus_endpoint(bus: BusSerializer, db: Session = Depends(get_db)):
    db_bus = Bus(
        lineNumber=bus.lineNumber,
        with_slash=bus.with_slash,
        starting=bus.starting,
        destination=bus.destination,
        garage=bus.garage
    )
    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)
    return { "message": "Bus created successfully", "bus": db_bus }

@app.get("/buses/", status_code=status.HTTP_200_OK)
def get_bus_endpoint(db: Session = Depends(get_db)):
    buses = db.query(Bus).all()
    if buses is None or len(buses) == 0:
        raise HTTPException(status_code=404, detail={"error_message": "No buses found"})
    return { "message": "Buses found", "buses": buses }


@app.get("/buses/id/{bus_id}", status_code=status.HTTP_200_OK)
def get_bus_by_id_endpoint(bus_id: int, db: Session = Depends(get_db)):
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if bus is None:
        raise HTTPException(status_code=404, detail={"error_message": "Bus with supplied details not found"})
    return { "message": "Bus found", "bus": bus }

@app.get("/buses/line/{bus_lineNumber}", status_code=status.HTTP_200_OK)
def get_bus_by_lineNumber_endpoint(bus_lineNumber: int, db: Session = Depends(get_db)):
    buses = db.query(Bus).filter(Bus.lineNumber == bus_lineNumber).all()
    if buses is None or len(buses) == 0:
        raise HTTPException(status_code=404, detail={"error_message": "Bus with supplied details not found"})
    return { "message": "Buses found", "buses": buses }

@app.get("/buses/line/{bus_lineNumber}/with_slash/{with_slash}", status_code=status.HTTP_200_OK)
def get_bus_by_lineNumber_and_with_slash_endpoint(bus_lineNumber: int, with_slash: bool, db: Session = Depends(get_db)):
    bus = db.query(Bus).filter(Bus.lineNumber == bus_lineNumber, Bus.with_slash == with_slash).first()
    if bus is None:
        raise HTTPException(status_code=404, detail={"error_message": "Bus with supplied details not found"})
    return { "message": "Bus found", "bus": bus }

@app.put("/buses/line/{bus_lineNumber}/with_slash/{with_slash}", status_code=status.HTTP_200_OK)
def update_bus_by_lineNumber_and_with_slash_endpoint(bus_lineNumber: int, with_slash: bool, bus: BusSerializer, db: Session = Depends(get_db)):
    db_bus = db.query(Bus).filter(Bus.lineNumber == bus_lineNumber, Bus.with_slash == with_slash).first()
    if db_bus is None:
        raise HTTPException(status_code=404, detail={"error_message": "Bus with supplied details not found"})

    db_bus.starting = bus.starting
    db_bus.destination = bus.destination
    db_bus.garage = bus.garage

    db.commit()
    db.refresh(db_bus)
    return { "message": "Bus updated successfully", "bus": db_bus }

@app.delete("/buses/line/{bus_lineNumber}/with_slash/{with_slash}", status_code=status.HTTP_200_OK)
def delete_bus_by_lineNumber_and_with_slash_endpoint(bus_lineNumber: int, with_slash: bool, db: Session = Depends(get_db)):
    db_bus = db.query(Bus).filter(Bus.lineNumber == bus_lineNumber, Bus.with_slash == with_slash).first()
    if db_bus is None:
        raise HTTPException(status_code=404, detail={"error_message": "Bus with supplied details not found"})

    db.delete(db_bus)
    db.commit()
    return { "message": "Bus deleted successfully" }