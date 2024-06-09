
from scraper import Scraper
from dboperations import create_tables,reset_database

if __name__=="__main__": 
    
    # creating tables
    create_tables()

    # reseting old database records
    reset_database()

    s = Scraper()

    #starting scraping
    s.start()