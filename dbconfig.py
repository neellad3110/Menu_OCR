from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


DATABASE_URL = 'mysql+mysqlconnector://root:mysql123@localhost/MumbaiRestaurants'

try:
    # Creating the database engine
    engine = create_engine(DATABASE_URL, echo=True)

    # Creating a new session factory
    Session = scoped_session(sessionmaker(bind=engine))

except Exception as e :
    print("An error encountered while connecting to the database.",e)
    exit(0)



def get_session():
    return Session()

def close_session():
    session=get_session()
    session.close()





