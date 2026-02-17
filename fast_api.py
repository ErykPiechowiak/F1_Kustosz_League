from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import select, distinct
from database import RaceResult, get_session, QualiResult
from typing import Optional
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # później możesz zawęzić
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/", StaticFiles(directory="build/web", html=True), name="web")

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


@app.get("/drivers_in_season_{season}", dependencies=[Depends(check_token)])
def get_drivers(season: int, db: Session = Depends(get_session)):
    query = (
        select(distinct(RaceResult.player_name))
        .where(RaceResult.season == season)
        .order_by(RaceResult.player_name)
    )

    result = db.execute(query).scalars().all()
    return result

@app.get("/driver-stats-races/{season}/{driver}", dependencies=[Depends(check_token)])
def get_drivers(season: int, driver: str, db: Session = Depends(get_session)):
    query = (
        select(RaceResult)
        .where(
            RaceResult.season == season,
            RaceResult.player_name == driver
        )
        .order_by(RaceResult.round_nr)
    )

    result = db.execute(query).scalars().all()
    return result

@app.get("/driver-stats-qualis/{season}/{driver}", dependencies=[Depends(check_token)])
def get_drivers(season: int, driver: str, db: Session = Depends(get_session)):
    query = (
        select(QualiResult)
        .where(
            QualiResult.season == season,
            QualiResult.player_name == driver
        )
        .order_by(QualiResult.round_nr)
    )

    result = db.execute(query).scalars().all()
    return result