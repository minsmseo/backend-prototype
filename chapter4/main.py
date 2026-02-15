from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from datetime import date

import crud, schemas
from datebase import SessionLocal

app = FastAPI()

# 종속성
def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message:": "API 상태 확인 성공"}

@app.get("/v0/players/",response_model=list[schemas.Player])
def read_players(skip: int=0,
                limit: int =100,
                minimum_last_changed_date: date=None,
                first_name: str=None,
                last_name: str=None,
                db:Session = Depends(get_db)):
    players = crud.get_players(db,
                               skip=skip,
                               limit=limit,
                               min_last_changed_date=minimum_last_changed_date,
                               first_name=first_name,
                               last_name=last_name)
    return players

@app.get("/v0/players/{player_id}",response_model=schemas.Player)
def read_player(player_id: int, db:Session = Depends(get_db)):
    player = crud.get_player(db,player_id=player_id)
    if player is None:
        raise HTTPException(status_code = 404, detail="선수를 찾을 수 없습니다.")
    return player
