from typing import Optional
from contextlib import asynccontextmanager
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


@asynccontextmanager #replace for the on_event's error.
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield  


app = FastAPI(lifespan=lifespan)


@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
    pass


@app.get("/heroes/{name}")
def get_hero(name: str):
    with Session(engine) as session:
        get = select(Hero).where(Hero.name == "{name}")
        hero = session.exec(get).first()
        if hero is None:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero
    pass


@app.get("/heroes/")
def get_heroes():
    with Session(engine) as session:
        get_all = select(Hero)
        all_heroes = session.exec(get_all).all()
        print(all_heroes)
    pass
