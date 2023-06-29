from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine, select , text ,exists, column
from sqlalchemy.orm import sessionmaker
from db.config import psql
from sqlalchemy.orm import class_mapper
import db.models
import os


engine = create_engine(f"postgresql://{psql['pguser']}:{psql['pgpasswd']}@{psql['pghost']}:{psql['pgport']}/{psql['pgdb']}")

def create_database_from_sql(engine):
    print(os.path.split(__file__)[0] + ".sql")
    with engine.connect() as con:
        with open(os.path.split(__file__)[0] + "/db.sql") as file:
            query = text(file.read())
            con.execute(query)
            con.commit()


def get_engine():
    url = f"postgresql://{psql['pguser']}:{psql['pgpasswd']}@{psql['pghost']}:{psql['pgport']}/{psql['pgdb']}"
    
    if not database_exists(url):
        create_database(url)
    return create_engine(url,pool_size=50, echo=False)

def create_tables():
    engine = get_engine()
    create_database_from_sql(engine)


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

session = get_session()


def add_(table:object, json:dict):
    obj = table(**json)
    check = session.query(table).filter_by(**json).first()
    if check:
        return check
    session.add(obj)
    session.commit()
    return obj

def get_(table:object,**target):
    try:
        return session.query(table).filter_by(**target).first()
    except Exception as e:
        print(e)
        return None
    

def get_primary_key(obj):
    mapper = class_mapper(obj.__class__)
    primary_keys = [prop.key for prop in mapper.primary_key]
    return {key: getattr(obj, key) for key in primary_keys}

def get_by_str(table: str, id):
    try:

        table = db.models.__dict__.get(table.capitalize())

        return session.query(table).filter_by(id=id).first()
    except Exception as e:
        print(e)
        return None

    
def gets_(table:object,limit = None,**target,):
    try:
        if not limit:
            return session.query(table).filter_by(**target).all()
        else:
            return session.query(table).filter_by(**target).limit(limit).all()
    except Exception:
        return None


def remove_records_from_(table:object):
    session.query(table).delete()
    session.commit()


# if __name__ == "__main__":
#     #create_tables()
#     # remove_records_from_(models.Embroidery)