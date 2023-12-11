from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select

# Importing base class of SQLModel, and base class of Field.
# Session: a manager of different session (Session pool).
# Usually a DB is TCP connection and in a particular application, usually you want to have a connection pool. It is like a pool (black box)
# and inside, you can have a few connections and will be kept alive. Everytime you want to use it, you pick the connection
# from the connection pool, write to it, then return it to the connection pool. Therefore, we don't have to spend so much time doing ACK and SYN
# TCP connection.
# The way it works: when you initialise the app, we are going to create a few connection ready to use, and we keep it alive, (same as above).
# If we do this way, we don't need to create an destroy connections all the time, and save a lot of latency (everytime we create a DB
# connection, we need to authenticate, and keep the connection alive, use it, close it, a part of flow of opening it and getting acknowledement
# for closing it takes lots of time).
# Many parts of your programme will use the same connection pool.


class Hero(SQLModel, table=True):
    # Create a new class - Implementing DAO class because it is inheriting from the SQLModel class.
    # It means to represent an actual entry inside the database.
    # Below: We define a few fields.
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

    # Break down those fields above:
    # Hero table has by default is a primary key, but the id can be optional (having it or not))
    # Name must be compulsory
    # Secret name must be compulsory
    # Age can be optional (having it or not)
    # If you decide to connect to a particular database, which you define later, Id is optional because it will be out to sequential.

    # The reason why we say in line 13: "default = None"
    # because we don't want to make the DAO fixed taped on a particular values of ID when it hasn't talked to the DB or inserted the entry to the DB yet.
    # Therefore, the ID is actually only found out after you insert into the DB.
    # It means when you create a DAO model, you don't need to specify the ID as the DB will tell you what the ID is, you don't need to tell.


# ------------------------------------------------------------------------

hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

# We create a few DAO objects but we haven't inserted them into the DB.

# ------------------------------------------------------------------------

# We create an object for the engine.
engine = create_engine("sqlite:///database.db")

# ------------------------------------------------------------------------

# We create/ initialise a connection pool (the line below)
SQLModel.metadata.create_all(engine)

# ------------------------------------------------------------------------

# Taking a particular session out of ther session pool:
# with Session(engine) as session:
#     session.add(hero_1)
#     session.add(hero_2)
#     session.add(hero_3)
#     session.commit()

# Only when we commit, it is when we actually translate the DAO into SQL command, seal them together
# (as we can submit multiple SQL command at once), and finally commit.

# ------------------------------------------------------------------------

with Session(engine) as session:
    statement = select(Hero).where(Hero.name == "Spider-Boy")
    heroes = session.exec(statement).all()  # Get back the list for all. Here is a list of DAO "hero": List[Hero]
    print(heroes)
    print(type(heroes))
    
    hero = session.exec(statement).first() #Get back only one object.
    print(hero)

# What we do now:
# - We are looking for a hereo with name "Spider-Boy"
# - Then we execute the session and get the first answer only back (as we run main.py file twice before, so there is a duplicate in the DB)
# - Use .first() or .all(), depending on whether you want to print the first answer only or print all answers which match the conditions.
# In all of this process, it will automatically translate into a SQL query first. With the SQL answers they get, it will pass it into JSON,
# then once it has JSON, it will pass into the DAO.
# What we print out in the terminal, is the actual DAO's content.

# ------------------------------------------------------------------------


