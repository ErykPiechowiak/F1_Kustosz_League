from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import RaceResult, get_session, QualiResult
from typing import Optional
import os

app = FastAPI()

# PROSTY TOKEN
TOKEN = os.getenv("API_TOKEN")
security = HTTPBearer()


def check_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials.credentials != TOKEN:
        raise HTTPException(status_code=401, detail="Nieprawidłowy token")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/results", dependencies=[Depends(check_token)])
def get_results(
    race: Optional[str] = None,
    db: Session = Depends(get_session)):
    query = db.query(RaceResult)
    if race:
        query = query.filter(RaceResult.race == race)
        
    results = query.all()

    return [
        {
            "id": r.id,
            "season": r.season,
            "round_nr": r.round_nr,
            "driver": r.player_name,
            "team": r.constructor_name,
            "track_name": r.track_name,
            "position": r.position,
            "time": r.time,
            "fastest_lap": r.fastest_lap,
            "points": r.points,
        }
        for r in results
    ]

@app.get("/quali_results", dependencies=[Depends(check_token)])
def get_quali_results(
    track_name: Optional[str] = None,
    db: Session = Depends(get_session)):
    query = db.query(QualiResult)
    if track_name:
        query = query.filter(QualiResult.track_name == track_name)
        
    results = query.all()

    return [
        {
            "id": r.id,
            "season": r.season,
            "round_nr": r.round_nr,
            "driver": r.player_name,
            "team": r.constructor_name,
            "track_name": r.track_name,
            "quali_time": r.quali_time,
        }
        for r in results
    ]
