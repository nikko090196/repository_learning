from typing import Optional, List

# from contextlib import asynccontextmanager (replace for the on_event's error/deprecated)
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# The instructor's code but VSCode crossed out on_event, and recommended to use lifespan handler.
# Therefore, I commented out his code and replaced with new one.
# app = FastAPI()
# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


# @asynccontextmanager  # replace for the on_event's error/deprecated
# async def lifespan(app: FastAPI):
#     create_db_and_tables()
#     yield


app = (
    FastAPI()
)  # app=FastAPI(lifespan=lifespan) (replace for the on_event's error/deprecated)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
    pass


# Create a new SQModel and it does not represent a new table, we just use it to augment the pathway we can change an existing DAO in DB
# This is a specialised SQModel class only for the Update Operations.
# Eg. Hero table (DAO: table, True) has:
# - Class: Hero Update (This is DTO - a new way to do DTO in SQ) - having some info but also the updated one.
# - Class: Hero Create (This is DTO - a new way to do DTO in SQ) - having some info but not all info
# * More about DTO above: It is just to defind a payload for what information you need when you wanna have an update operation.
# SQModel is just an inherited class of pydantic
class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None


# Use API to look up by using different DTO for different operation. Later on, we can return DAO.
# We can customeise DTO differently.
@app.patch(
    "/hero/", response_model=Hero
)  # Opening a new session, try to get the hero by hero's name:
def change_secret_name(hero_update: HeroUpdate):  # passing the hero_update object
    with Session(engine) as session:
        db_hero = session.exec(
            select(Hero).where(Hero.name == hero_update.name)
        ).first()  # trying to GET API. #db_hero: current
        if not db_hero:  # if you cannot find the hero, say "Hero not found"
            raise HTTPException(status_code=404, detail="Hero not found")
        # return db_hero # we don't change anything, we just try to look it up using the DTO => Demonstrating that we are getting info using
        # different request body than actual DAO. #and return the db_hero with hero's name.
        hero_data = hero_update.dict(
            exclude_unset=True
        )  # convert hero_update, which is the data we want to override, into a dict. #hero_data: input
        for (
            key,
            value,
        ) in hero_data.items():  # for each key-value pair in the input dict
            setattr(
                db_hero, key, value
            )  # we are gonna change the attribute of the hero obj that we just got
        session.add(db_hero)  # override
        session.commit()
        session.refresh(db_hero)
        return db_hero


@app.get(
    "/heroes/{name}", response_model=Hero
)  # type hint will be different from native pydantic model
def get_hero(name: str):
    with Session(engine) as session:
        get = select(Hero).where(Hero.name == name)
        hero = session.exec(get).first()
        if hero is None:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero
    pass


@app.get("/heroes/", response_model=List[Hero])
def get_heroes():
    with Session(engine) as session:
        get_all = select(Hero)
        all_heroes = session.exec(get_all).all()
        print(all_heroes)
    pass
