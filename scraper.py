from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from preprocess import add_to_restaurant,process_OCR,add_to_menu,preprocess_image
from dbconfig import close_session

class Scraper:
     

    MAIN_URL='https://www.zomato.com'           # mail domain url
    SLEEP_TIME=2                                # sleeping time 
    SCROLL_PAUSE_TIME = 3                       # scroll sleeping time
 

    def get_restro_list_url(self):
        """
        functions concats main url with other url part
        """
        return self.MAIN_URL+'/mumbai/restaurants'
    
    def get_restro_url(self,innerURL):
        """
        function concats main url with inner url variale which has restaurant url part
        """
        return self.MAIN_URL+innerURL


    def get_restaurant_menu(self,inner_driver,menu_cards,restaurant_id):
        """
        function is reposible for scraping , OCR processing and inserting data of menu images.
        """
        for card in menu_cards :
            # opening mennu card
            inner_driver.execute_script("arguments[0].click();", card);

            
            try :
                time.sleep(self.SLEEP_TIME)
                card_preview_close_div=inner_driver.find_element(By.CLASS_NAME,"gUpPcI")
                card_preview_close_icon=card_preview_close_div.find_element(By.TAG_NAME,'i')
            
                card_preview_right_arrow_div=inner_driver.find_element(By.CLASS_NAME,"iZkCOf")
                card_preview_right_arrow_icon=card_preview_right_arrow_div.find_element(By.TAG_NAME,'i')       


                while card_preview_right_arrow_icon.is_displayed():

                    card_preview_image_url_div=inner_driver.find_element(By.CLASS_NAME,"iMLdZd")
                    card_preview_image_url=card_preview_image_url_div.find_element(By.TAG_NAME, 'img').get_attribute('src').rsplit('?',1)[0]

                    image = preprocess_image(card_preview_image_url)
                    process_OCR(image)
                    card_preview_right_arrow_icon.click()
                    time.sleep(self.SLEEP_TIME)
                    
            except Exception as e: 

                card_preview_image_url_div=inner_driver.find_element(By.CLASS_NAME,"iMLdZd")
                card_preview_image_url=card_preview_image_url_div.find_element(By.TAG_NAME, 'img').get_attribute('src').rsplit('?',1)[0]
                image=preprocess_image(card_preview_image_url)
                process_OCR(image)
                card_preview_close_icon.click()
                time.sleep(self.SLEEP_TIME)

            add_to_menu(restaurant_id)    


    def start(self):
        """
        function is responsible for driver initialzing, scarping,scrolling controll and locating menu section of restaurant 
        """
        outer_driver = webdriver.Firefox()
        outer_driver.get(self.get_restro_list_url())

        time.sleep(self.SLEEP_TIME)
        screen_height = outer_driver.execute_script("return window.screen.height;")


        screen_height = outer_driver.execute_script("return window.screen.height;") 

        inner_driver = webdriver.Firefox()

        SCROLL_COUNT=1

        count =1;
        try :

            while True :

                outer_driver.execute_script("window.scrollTo(0, {screen_height}*{count});".format(screen_height=screen_height, count=SCROLL_COUNT))
                
                SCROLL_COUNT +=1
                time.sleep(self.SCROLL_PAUSE_TIME)

                scroll_height = outer_driver.execute_script("return document.body.scrollHeight;")

                if (screen_height) * SCROLL_COUNT > scroll_height :
                    break

                outer_soup = BeautifulSoup(outer_driver.page_source, "html.parser")

                restaurant_divs = outer_soup.findAll('div', class_='jumbo-tracker')

                for parent in restaurant_divs :

                    restaurant_menu_url = parent.find("a").get('href').rsplit('/', 1)[0] + '/menu'
                    inner_driver.get(self.get_restro_url(restaurant_menu_url))
                    
                    restaurant_profile_div= inner_driver.find_element(By.CLASS_NAME,"fPpMAv")
                    restaurant_name = restaurant_profile_div.find_element(By.TAG_NAME,'h1').text
                    restaurant_address = restaurant_profile_div.find_element(By.CLASS_NAME,'vNCcy').text
                    
                    try :

                        menu_card_types=inner_driver.find_elements(By.CLASS_NAME,'cgNeOC')
                        restaurant_id=add_to_restaurant(restaurant_name,restaurant_address)
                        self.get_restaurant_menu(inner_driver,menu_card_types,restaurant_id)
                        count+=1


                    except :
                        continue
        finally:                   
            close_session()           
            inner_driver.quit()
            outer_driver.quit()
            
        