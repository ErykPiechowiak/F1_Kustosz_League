from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import RaceResult, get_session
from typing import Optional

app = FastAPI()

# PROSTY TOKEN
TOKEN = "f1-league-secret-123"
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
            "driver": r.driver,
            "team": r.team,
            "race": r.race,
            "position": r.position,
            "gap_to_leader": r.gap_to_leader,
            "points": r.points,
        }
        for r in results
    ]

