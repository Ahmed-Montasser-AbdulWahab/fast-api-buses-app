from fastapi import FastAPI, Response, status, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from db_models import MicroBus, Base
from serializer_models import MicroBus as MicrobusSerializer

def init_db():
    db = SessionLocal()
    try:
        db_buses = [
                MicroBus(
                    starting="First Settlement",
                    destination="Tahrir"
                ),
                MicroBus(
                    starting="Matbaa",
                    destination="Masakn Ain Shams"
                )
                ]
        db_buses_count = db.query(MicroBus).count()

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

@app.post("/micro-buses", status_code=status.HTTP_201_CREATED)
def create_bus_endpoint(bus: MicrobusSerializer, db: Session = Depends(get_db)):
    db_bus = MicroBus(
        starting=bus.starting,
        destination=bus.destination
    )
    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)
    return { "message": "Microbus created successfully", "bus": db_bus }

@app.get("/micro-buses", status_code=status.HTTP_200_OK)
def get_bus_endpoint(db: Session = Depends(get_db)):
    buses = db.query(MicroBus).all()
    if buses is None or len(buses) == 0:
        raise HTTPException(status_code=404, detail={"error_message": "No microbuses found"})
    return { "message": "Microbuses found", "buses": buses }


@app.get("/micro-buses/{id}", status_code=status.HTTP_200_OK)
def get_bus_by_id_endpoint(id: int, db: Session = Depends(get_db)):
    bus = db.query(MicroBus).filter(MicroBus.id == id).first()
    if bus is None:
        raise HTTPException(status_code=404, detail={"error_message": "Microbus with supplied details not found"})
    return { "message": "Microbus found", "bus": bus }

@app.put("/micro-buses/{id}", status_code=status.HTTP_200_OK)
def update_bus_by_id_endpoint(id: int, bus: MicrobusSerializer, db: Session = Depends(get_db)):
    db_bus = db.query(MicroBus).filter(MicroBus.id == id).first()
    if db_bus is None:
        raise HTTPException(status_code=404, detail={"error_message": "Microbus with supplied details not found"})

    db_bus.starting = bus.starting
    db_bus.destination = bus.destination

    db.commit()
    db.refresh(db_bus)
    return { "message": "Microbus updated successfully", "bus": db_bus }

@app.delete("/micro-buses/{id}", status_code=status.HTTP_200_OK)
def delete_bus_by_id_endpoint(id: int, db: Session = Depends(get_db)):
    db_bus = db.query(MicroBus).filter(MicroBus.id == id).first()
    if db_bus is None:
        raise HTTPException(status_code=404, detail={"error_message": "Microbus with supplied details not found"})

    db.delete(db_bus)
    db.commit()
    return { "message": "Microbus deleted successfully" }