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
# from numba import jit, float32
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
table.write(0, 1, 'IDS')
table.write(0, 2, 'NAMES')
table.write(0, 3, 'IMAGES')




# https://www.amazon.in/Nivia-Shining-Star-2022-Football-White/dp/B00363WZY2

data = pd.read_excel(r'C:\Users\Nagababu\Downloads\LMWK01_CT_NHB.xlsx')
product = pd.DataFrame(data)

ids = product['asin'].tolist()
names = product['asin_name'].tolist()
# print(names)
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36'
    }    
    # , columns= ['urls']
# searchProducts = product['products'].tolist()

# url = "https://www.amazon.in/Nivia-Shining-Star-2022-Football-White/dp/B00363WZY2"

# @jit(nopython = True)
def scrapyingImages(url,Type):
    driver = webdriver.Chrome(r'C:\chromedriver.exe')
    driver.get(url) 
            # this is just to ensure that the page is loaded
            
    time.sleep(5)
    html = driver.page_source
    # soup = BeautifulSoup(f.content, 'lxml')
    # images = soup.find_all('span',{
    #     'class':'a-button-text'
    # })
    # ['a-unordered-list' ,'a-nostyle', 'a-button-list','a-vertical','a-horizontal','a-spacing-top-micro','regularAltImageViewLayout']
    soup = BeautifulSoup(html, 'html.parser')
    driver.close()
    # images = soup.find('ul',{'class': "a-unordered-list a-nostyle a-horizontal list maintain-height"}).find_all('div',{
    #     'class': "imgTagWrapper"
    # })
    if(Type==str):
        images = soup.find_all('div',{
            'class': "imgTagWrapper"
        })
        img_list = []
        img_src = []
        for i in images:
            print(i.img,'..............')
        for i in images:
            if(i.img != None):
                img_list.append(i.img)
        for k in img_list:
            y = k['src'] + ','
            img_src.append(y)
        
        return img_src 
    else:
        imgList = []
        img_src = []
        images = soup.find('div',{
            'class': "maintain-height"
        })

        print(images.img,'jjdadjabaabdbjdbajabsjssjasjssjs')
        # if(images!= None):
        # #     imgList.append(i.img) 
        #     for y in images:
        #         m = str(y['src']) + ','
        #         print(m)
        #         img_src.append(m)
        val = images.img['src'] + ','
        return val  
            





# f = requests.get(url, headers = headers,allow_redirects=False)
# print(f)

# 'html.parser'
# @jit(nopython = True)
def mainFunction(ID,Type):

    URL = 'https://www.amazon.in/s?k=' + str(ID)
    # f = requests.get(URL, headers = headers,allow_redirects=False)

    # soup = BeautifulSoup(f.content, 'lxml')

    # anchorLink = soup.find('a',{'class': 
    # 'a-link-normal s-no-outline'})
    # print(anchorLink)
    driver = webdriver.Chrome(r'C:\chromedriver.exe')
    driver.get(URL)
            # this is just to ensure that the page is loaded
            
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.close()
    anchorLink = soup.find('a',{'class': 
    'a-link-normal s-no-outline'})
    
    if(anchorLink!=None):
        val = 'https://www.amazon.in' + str(anchorLink['href'])
        resultImages = scrapyingImages(val,Type)
        return resultImages
    else:
        return 'NotFound'    

    # soup = BeautifulSoup(f.content, 'lxml')
    # images = soup.find_all('span',{
    #     'class':'a-button-text'
    # })
    # soup = BeautifulSoup(html, 'html.parser')
    

    

row = 1

resultImagesList = []
for i in range(len(ids)):
    ID = ids[i]
    val = type(ID)
    print(ID,i)
    value = mainFunction(ID,val)
    print(value)
    resultImagesList.append(value)
  
for my in range(len(resultImagesList)):
    Id = str(ids[my])
    v1 = Id.replace(" ", "")
    v2 = names[my]
    v3 = resultImagesList[my]
    table.write(row, 0, row)
    table.write(row, 1, v1)
    table.write(row, 2, v2)  
    table.write(row, 3, v3)

    row+=1 
workbook.save('scraper-data-LMWK01_CT_NHB.xls')   










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
