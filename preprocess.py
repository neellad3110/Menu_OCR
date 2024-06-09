import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
import pandas as pd
import requests
import re
from dboperations import insert_menu,insert_restaurant

restaurant_menu_store=pd.DataFrame(columns=['Item','Price'])  # for storeing each menu card of a individual restaursnts


def preprocess_image(url):
    """
    this function is responsible for cleaning images as per backgrond and applying filters to interpreat text
    """ 
    response = requests.get(url)
    img = np.asarray(bytearray(response.content), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR) 

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Determine the background type
    background_type = determine_background_type(gray)

    # Invert colors if the background is dark
    if background_type == "dark_background":
        gray = cv2.bitwise_not(gray)
        return gray

    # Apply sharpening
    # sharpened = sharpen_image(gray)

    return gray


def determine_background_type(gray_image):
    """
    this function is responsible for checking background of image as light or dark
    """
    # Calculate the average pixel intensity
    avg_intensity = np.mean(gray_image)
    # Define a threshold to determine background type
    threshold = 127
    if avg_intensity > threshold:
        return "light_background"
    else:
        return "dark_background"
    

def process_OCR(preprocessed_img):

    """
    this function is responsible for OCR processing of image
    """
    config = r'--oem 1 -l eng --psm 4'

    #  for windows user  please uncomment the below line , add your tesseract installation path. 
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract_OCR\tesseract.exe'

    text = pytesseract.image_to_string(preprocessed_img, config=config)
    # Separating text and numbers in OCR text output
    separate_text_and_number(text)
    

def separate_text_and_number(text):
    """
    this function is responsible for seperating string and number parts in OCR text and storing in menu dataframe.
    """
    global restaurant_menu_store

    lines = text.split('\n')

    for line in lines:
        if line.strip():  # Ensure the line is not empty
            match = re.search(r'(\d+)$', line)
            if match:
                number = int(match.group(0))
                text_part = line[:match.start()].strip()
            else:
                number = 0
                text_part = line.strip()

            new_row = pd.DataFrame({'Item': [text_part], 'Price': [number]})
            restaurant_menu_store = pd.concat([restaurant_menu_store, new_row], ignore_index=True)

    clean_menu()


# def sharpen_image(image):
#     # Define a sharpening kernel
#     kernel = np.array([[0, -1, 0], 
#                        [-1, 5, -1], 
#                        [0, -1, 0]])
#     # Apply the sharpening kernel to the input image
#     sharpened = cv2.filter2D(image, -1, kernel)
#     return sharpened

def clean_menu():
    """
    this function is responsible for cleaning data frame items Empty fields and price with 0 field
    """
    global restaurant_menu_store

    restaurant_menu_store = restaurant_menu_store[restaurant_menu_store['Item'] != '']
    restaurant_menu_store = restaurant_menu_store[restaurant_menu_store['Price'] != 0]


def add_to_restaurant(name,address):
    """
    This function is responsible for performing insertion, operation of restaurant and returning restaurant ID
    """
    restaurant_id = insert_restaurant(name,address)
    return restaurant_id

def add_to_menu(restaurant_id):
    """
    this function is responsible for inserting restaurant menu, data in database and  after operation removing data from the data frame
    """
    global restaurant_menu_store

    for index, row in restaurant_menu_store.iterrows():
        insert_menu(restaurant_id,row['Item'],row['Price'])

    restaurant_menu_store = restaurant_menu_store.iloc[0:0]  

