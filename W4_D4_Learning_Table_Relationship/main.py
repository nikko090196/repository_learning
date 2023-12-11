from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class TeamBase(
    SQLModel
):  # Table: DTO - This a common class (Line 7 - 9). Not only Team class below, but other DTO and DAO to inherit from.
    name: str = Field(index=True)
    headquarters: str


class Team(
    TeamBase, table=True
):  # Table: DAO - actual definition for table Team. And Team inherits all properties from Team Base.
    id: Optional[int] = Field(default=None, primary_key=True)

    heroes: List["Hero"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):  # DTO inherits from TeamBase for Create operation
    pass


class TeamRead(TeamBase):  # DTO inherits from TeamBase for Read operation
    id: int


class TeamUpdate(SQLModel):  # DTO inherits from TeamBase for Update operation
    name: Optional[str] = None
    headquarters: Optional[str] = None


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):  # DAO of HeroBase
    id: Optional[int] = Field(default=None, primary_key=True)

    team: Optional[Team] = Relationship(back_populates="heroes")


class HeroRead(HeroBase):  # DTO inherits from HeroBase for Read operation
    id: int


class HeroCreate(HeroBase):  # DTO inherits from HeroBase for Create operation
    pass


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[int] = None


sqlite_file_name = "relationship.db" #We define we are gonna get from a file called relationship.db
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables(): #Create table, initialisation.
    SQLModel.metadata.create_all(engine)


def get_session(): #Get a session, implement generator for the session => Indenpendency Injection
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/", response_model=HeroRead)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate): #HeroCreate is DTO as an input, process it and put it below, into
    db_hero = Hero.from_orm(hero) #into DAO, and save DAO into DB.
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=List[HeroRead])
def read_heroes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0, #offset - limit: If you have a long list of query result, 
    #and you don't want to run the query for too long, and you want to stop somewhere not to throttle on to the session
    #and be able to build pages and load pages instead of blowing long file.
    #Offset: Moving on to the next offset and so on.
    #Limit: We turn by default only 100 at the time for you.
    limit: int = Query(default=100, le=100),
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all() #offset-limit: read 100 at once, 100 at once.
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroRead)
def read_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(
    *, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate
):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.delete("/heroes/{hero_id}")
def delete_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}


@app.post("/teams/", response_model=TeamRead)
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    db_team = Team.from_orm(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.get("/teams/", response_model=List[TeamRead])
def read_teams(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@app.get("/teams/{team_id}", response_model=TeamRead)
def read_team(*, team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.patch("/teams/{team_id}", response_model=TeamRead)
def update_team(
    *,
    session: Session = Depends(get_session),
    team_id: int,
    team: TeamUpdate,
):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.delete("/teams/{team_id}")
def delete_team(*, session: Session = Depends(get_session), team_id: int):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}
