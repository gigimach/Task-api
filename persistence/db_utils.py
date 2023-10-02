from sqlmodel import create_engine, SQLModel

def get_engine():
    db_url = "sqlite:///database.db"
    return create_engine(db_url, echo=True)


def create_tables():
    SQLModel.metadata.create_all(get_engine())