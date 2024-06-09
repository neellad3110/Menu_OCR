## About
The purpose of this project is store food menu items and their price of various restaurants in Mumbai. 

Data is collected using Zomato's online food delivery website for restraunts in Mumbai [here](https://www.zomato.com/mumbai/restaurants)

Using Tesseract OCR food menu items and their prices are stored in MYSQL database.

## Installation

Fork this repository to your github account  and clone the forked repository and proceed with steps mentioned below

```
https://github.com/neellad3110/Menu_OCR.git
```

### 1. Firefox Browser :
This project uses Firefox driver for scraping data.
#### For MacOs :

```
https://www.mozilla.org/en-US/firefox/mac/
```
#### For Windows

```
https://www.mozilla.org/en-US/firefox/windows/
```

### 2. Python installation :

Head over to the [official Python website](https://www.python.org/downloads/) and download the installer
Also, be sure to have `git` downloaded and available in your PATH as well.

### 3. MySQL installation :

[MySql](https://dev.mysql.com/downloads/installer/) is available for download as ready-to-use packages or installers for various platforms.

### 4. Tesseract OCR Installation :

#### For MacOs :

```
brew install tesseract
```
#### For Windows

```
https://github.com/UB-Mannheim/tesseract/wiki
```

Note : For Windows users, you need to uncomment the line `tesseract_cmd` in the [preprocess.py](preprocess.py) file to point to the Tesseract-OCR executable the path at line 60. 

### 5. Create Database in MySQL

Upadte your Database configuration is [dbconfig.py](dbconfig.py) file.

### 6. Install project python libraries.

#### 6.1 Install Virtual Environment :
```    
pip install virtualenv
```
```
python -m venv venv
```

#### 6.2 Activate Virtual Envrionment :

##### For MacOs :
```
source venv/bin/activate
```
##### For Windows :
```
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process
```
```
.\venv\Scripts\Activate.ps1
```
6.3  Install pip packages :

```
pip install -r requirements.txt
```

## Run

Project will untill all the restraunts are covered.

```
python main.py
```

To stop the project press :

##### For Macos : Control(^) + C
##### For windows : Cntrl + C



