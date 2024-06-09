from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import List, Dict, Optional
from datetime import datetime
import uvicorn

app = FastAPI()

class Session(BaseModel):
    id: int
    title: str
    start_time: datetime
    end_time: datetime
    max_participants: int

    @field_validator("end_time")
    def end_time_after_start_time(cls, v, values):
        if "start_time" in values.data and v <= values.data["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v

class Participant(BaseModel):
    id: int
    name: str
    email: str

class Booking(BaseModel):
    participant_id: int
    session_id: int

class Conference(BaseModel):
    sessions: List[Session] = []
    participants: List[Participant] = []
    bookings: List[Booking] = []

conference = Conference()

@app.post("/add_session/")
def add_session(session: Session):
    for s in conference.sessions:
        if s.id == session.id:
            raise HTTPException(status_code=400, detail="Session with this ID already exists.")
    conference.sessions.append(session)
    return {"message": "Session added successfully", "session": session}

@app.post("/add_participant/")
def add_participant(participant: Participant):
    for p in conference.participants:
        if p.id == participant.id:
            raise HTTPException(status_code=400, detail="Participant with this ID already exists.")
    conference.participants.append(participant)
    return {"message": "Participant added successfully", "participant": participant}

@app.post("/book_session/")
def book_session(booking: Booking):
    # Check if participant exists
    participant = next((p for p in conference.participants if p.id == booking.participant_id), None)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    # Check if session exists
    session = next((s for s in conference.sessions if s.id == booking.session_id), None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Check if session is full
    current_bookings = [b for b in conference.bookings if b.session_id == booking.session_id]
    if len(current_bookings) >= session.max_participants:
        raise HTTPException(status_code=400, detail="Session is fully booked")

    # Check for overlapping bookings
    participant_bookings = [b for b in conference.bookings if b.participant_id == booking.participant_id]
    for pb in participant_bookings:
        booked_session = next((s for s in conference.sessions if s.id == pb.session_id), None)
        if booked_session:
            if not (session.end_time <= booked_session.start_time or session.start_time >= booked_session.end_time):
                raise HTTPException(status_code=400, detail="Participant already booked for an overlapping session")

    conference.bookings.append(booking)
    return {"message": "Session booked successfully", "booking": booking}

@app.get("/list_sessions/")
def list_sessions():
    return conference.sessions

@app.get("/list_participants/")
def list_participants():
    return conference.participants

@app.get("/list_bookings/")
def list_bookings():
    return conference.bookings

# uvicorn main:app --reload

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)