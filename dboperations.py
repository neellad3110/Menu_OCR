from dbmodel import Restaurants, Menu, Base
from dbconfig import get_session, close_session,engine

def create_tables():
    """
    Function is responsible for creating tables
    """
    Base.metadata.create_all(engine)

def insert_restaurant(name,address):
    """
    This function handles insertion operation of restaurants
    """
    session = get_session()
    try:
        new_restaurant = Restaurants(name=name,address=address)
        session.add(new_restaurant)
        session.commit()
        return new_restaurant.id
    
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()
def insert_menu(restaurant_id, item_name, price):
    """
    Dysfunction handles insertion, operation of restaurant menu
    """
    session = get_session()
    try:
        new_menu = Menu(restaurant_id=restaurant_id, item_name=item_name, price=price)
        session.add(new_menu)
        session.commit()
     
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()



def truncate_all_tables(engine):
    """
    This function will truncate all tables from the database
    """

    connection = engine.connect()
    trans = connection.begin()
    for table in reversed(Base.metadata.sorted_tables):
        connection.execute(table.delete())
    trans.commit()

# Main function to reset database
def reset_database():
    truncate_all_tables(engine)

def close_session():
    session = get_session()
    session.close()
   
           
    
