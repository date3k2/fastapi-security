from sqlmodel import create_engine, SQLModel, Session

# maybe url should be from env file
DATABASE_URL = "postgresql://postgres:date3k2@localhost:5432/postgres"
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
