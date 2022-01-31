import pandas as pd
from typing import List
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.sql.expression import and_, null
from sqlalchemy.sql.functions import user
from sharedlibrary import crud,models, schemas
from datetime import datetime, timedelta 
from sharedlibrary.database import SessionLocal, engine
from typing import Optional
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from xlwt import *
import os
import lxml
# import xlrd
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)
# wb = xlrd.open_workbook('C:/Users/Nagababu/Documents/products.xls')
app = FastAPI()
origins = [
    "http://127.0.0.1:8000/login",
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=1500)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    

pwd_context= CryptContext(schemes=["bcrypt"],deprecated='auto')


workbook = Workbook(encoding = 'utf-8')
table = workbook.add_sheet('data')
table.write(0, 0, 'S.no')
table.write(0, 1, 'Names')
table.write(0, 2, 'Investing')
table.write(0, 3, 'Mcx')
table.write(0, 4, 'economictimes')
table.write(0, 5, 'markets-businessinside')
table.write(0, 6, 'tradingeconomics')



# https://www.amazon.in/Nivia-Shining-Star-2022-Football-White/dp/B00363WZY2

data = pd.read_excel(r'C:\Users\Nagababu\Downloads\LMWK01_CT_NHB.xlsx')
product = pd.DataFrame(data)

ids = product['asin'].tolist()
names = product['asin_name'].tolist()
print(names)
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36'
    }    
    # , columns= ['urls']
# searchProducts = product['products'].tolist()






url = "https://www.amazon.in/Nivia-Shining-Star-2022-Football-White/dp/B00363WZY2"

# f = requests.get(url, headers = headers,allow_redirects=False)
# print(f)

# 'html.parser'

def mainFunction(ID,NAME):
    URL = 'https://www.amazon.in/' + NAME + 'dp/' + ID
    driver = webdriver.Chrome(r'C:\chromedriver.exe')
    driver.get(URL) 
            # this is just to ensure that the page is loaded
            
    time.sleep(5)
    html = driver.page_source
    # soup = BeautifulSoup(f.content, 'lxml')
    # images = soup.find_all('span',{
    #     'class':'a-button-text'
    # })
    soup = BeautifulSoup(html, 'html.parser')
    driver.close()
    images = soup.find('ul',{'class': 
    'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro regularAltImageViewLayout'}).find_all('span',{
        'class': "a-button-text"
    })
    img_list = []
    img_src = []
    for i in images:
        if(i.img != None):
            img_list.append(i.img)
    for k in img_list:
        img_src.append(k['src'])  
    return img_src    

num = 0
line = 0

for i in range(len(ids)):
    ID = ids[i]
    NAME = names[i]
    value = mainFunction(ID,NAME)
    print(value)










# for anchor in movies:
#     urls = 'https://www.rottentomatoes.com' + anchor['href']
#     movies_lst.append(urls)
#     num += 1
#     movie_url = urls
#     movie_f = requests.get(movie_url, headers = headers)
#     movie_soup = BeautifulSoup(movie_f.content, 'lxml')
#     movie_content = movie_soup.find('div', {
#     'class': 'movie_synopsis clamp clamp-6 js-clamp'
#     })
#     print(num, urls, '\n', 'Movie:' + anchor.string.strip())
#     print('Movie info:' + movie_content.string.strip())
#     table.write(line, 0, num)
#     table.write(line, 1, urls)
#     table.write(line, 2, anchor.string.strip())
#     table.write(line, 3, movie_content.string.strip())
#     line += 1
#     workbook.save('movies_top100.xls')



@app.post('/scrapper')
async def get_scrapper_data(file: UploadFile = File(...)):
    # productDetails = db.query(models.Movie).filter(models.Movie.title.contains(search)).all()

    data = pd.read_excel(file.file.read())
    product = pd.DataFrame(data)
    # , columns= ['urls']
    searchProducts = product['products'].tolist()
    return searchProducts
