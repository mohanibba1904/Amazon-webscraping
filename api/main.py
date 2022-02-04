from numpy import empty
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
from selenium.webdriver.chrome.options import Options
import time
from xlwt import *
import os
import lxml
import threading
# from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

options = webdriver.ChromeOptions()
options.headless = True


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

resultImagesList = []
a_dict = {}


# https://www.amazon.in/Nivia-Shining-Star-2022-Football-White/dp/B00363WZY2

data = pd.read_excel(r'C:\Users\Nagababu\Downloads\Home 15k.xlsx')
product = pd.DataFrame(data)

ids = product['asin'].tolist()
# ids = ['B07XS2SN44', 'B07X5V4DL1', 'B07X4Y7YTD', 'B0716ZHJRY', 'B07XLC41DF', 'B0716ZHJRY', 'B00JJH32Z0', 'B07YFX6V6M', 'B073BRD2BT', 'B07BSH63KT', 'B084GT7W7V', 'B07YFZJWB7', 'B07W93N9TR', 'B009UORBV8', 'B06Y526JKK', 'B00JJH32Z0', 'B07BPZTW2Z', 'B00A0ITZBW', 'B00JJH603Q', 'B07BSH63KT', 'B07YFX6V6M', 'B07NJK86KC', 'B07X4Y7YTD', 'B01MZC86UN', 'B07CZHZQNB', 'B07XRH8VQJ', 'B07CWTZVHV', 'B07W4RBP1C', 'B01A89OWHY', 'B07JP56R7R', 'B07TYPTSTM', 'B07GR5DF45', 'B07NQH4313', 'B01BC6LBGM', 'B01BC6CYK4', 'B01BC6HE6I', 'B01BC6YBGE', 'B01BC7KRWA', 'B06XYT4ZBP', 'B078W3XD6R', 'B07PWN2CYZ', 'B07W5VV6GT', 'B07NQJ61PK', 'B07XS41KX4', 'B077ZJX5W6', 'B07VTP2ZY1', 'B07BK678WN', 'B07WLT5T5P', 'B071CMHW33', 'B075ZTSX5Z', 'B07XX5TT95', 'B07GR5DF45', 'B07SRTF3TJ', 'B00F2GJ3NM', 'B00N3KF15S', 'B0171MA0U4', 'B07CRJJ93S', 'B07KKRT131', 'B07NJK86KC', 'B08238XFF2', 'B0786PQZPW', 'B07VF5ZB7Z', 'B07XS3GWDQ', 'B07XS4MKLF', 'B06XCMVZBS', 'B06XPCD87P', 'B07K6XRB4F', 'B0716ZHJRY', 'B07CZJWW9V', 'B07NQKCH4D', 'B07FZXS14Q', 'B07TTCK5CX', 'B07118K3RJ', 'B0754BXDLG', 'B07NQDTGF8', 'B07PVZR6TW', 'B07XRH8L9Y', 'B075ZSXXTN', 'B07MXZ4KDM', 'B08286YPGW', 'B07C98WHHM', 'B07C98WHHM', 'B082396FPD', 'B0796T6D49', 'B07KKRT131', 'B07NBDDH73', 'B07SZW944C', 'B07TTCLLX3', 'B07W5VTSBG', 'B07C98WHHM', 'B07T6NVXX1', 'B0168RQX40', 'B07B2SL53M', 'B07G5ZW6KN', 'B07TTCMPG6', 'B07X1QXGX1', 'B00F2GJ3NM', 'B079Z2G87Z', 'B07NQH4313', 'B07RCLBQ2P',
# 'B07XS2SN44', 'B07X5V4DL1', 'B07X4Y7YTD', 'B0716ZHJRY', 'B07XLC41DF', 'B0716ZHJRY', 'B00JJH32Z0', 'B07YFX6V6M', 'B073BRD2BT', 'B07BSH63KT', 'B084GT7W7V', 'B07YFZJWB7', 'B07W93N9TR', 'B009UORBV8', 'B06Y526JKK', 'B00JJH32Z0', 'B07BPZTW2Z', 'B00A0ITZBW', 'B00JJH603Q', 'B07BSH63KT', 'B07YFX6V6M', 'B07NJK86KC', 'B07X4Y7YTD', 'B01MZC86UN', 'B07CZHZQNB', 'B07XRH8VQJ', 'B07CWTZVHV', 'B07W4RBP1C', 'B01A89OWHY', 'B07JP56R7R', 'B07TYPTSTM', 'B07GR5DF45', 'B07NQH4313', 'B01BC6LBGM', 'B01BC6CYK4', 'B01BC6HE6I', 'B01BC6YBGE', 'B01BC7KRWA', 'B06XYT4ZBP', 'B078W3XD6R', 'B07PWN2CYZ', 'B07W5VV6GT', 'B07NQJ61PK', 'B07XS41KX4', 'B077ZJX5W6', 'B07VTP2ZY1', 'B07BK678WN', 'B07WLT5T5P', 'B071CMHW33', 'B075ZTSX5Z', 'B07XX5TT95', 'B07GR5DF45', 'B07SRTF3TJ', 'B00F2GJ3NM', 'B00N3KF15S', 'B0171MA0U4', 'B07CRJJ93S', 'B07KKRT131', 'B07NJK86KC', 'B08238XFF2', 'B0786PQZPW', 'B07VF5ZB7Z', 'B07XS3GWDQ', 'B07XS4MKLF', 'B06XCMVZBS', 'B06XPCD87P', 'B07K6XRB4F', 'B0716ZHJRY', 'B07CZJWW9V', 'B07NQKCH4D', 'B07FZXS14Q', 'B07TTCK5CX', 'B07118K3RJ', 'B0754BXDLG', 'B07NQDTGF8', 'B07PVZR6TW', 'B07XRH8L9Y', 'B075ZSXXTN', 'B07MXZ4KDM', 'B08286YPGW', 'B07C98WHHM', 'B07C98WHHM', 'B082396FPD', 'B0796T6D49', 'B07KKRT131', 'B07NBDDH73', 'B07SZW944C', 'B07TTCLLX3', 'B07W5VTSBG', 'B07C98WHHM', 'B07T6NVXX1', 'B0168RQX40', 'B07B2SL53M', 'B07G5ZW6KN', 'B07TTCMPG6', 'B07X1QXGX1', 'B00F2GJ3NM', 'B079Z2G87Z', 'B07NQH4313', 'B07RCLBQ2P',
# 'B07XS2SN44', 'B07X5V4DL1', 'B07X4Y7YTD', 'B0716ZHJRY', 'B07XLC41DF', 'B0716ZHJRY', 'B00JJH32Z0', 'B07YFX6V6M', 'B073BRD2BT', 'B07BSH63KT', 'B084GT7W7V', 'B07YFZJWB7', 'B07W93N9TR', 'B009UORBV8', 'B06Y526JKK', 'B00JJH32Z0', 'B07BPZTW2Z', 'B00A0ITZBW', 'B00JJH603Q', 'B07BSH63KT', 'B07YFX6V6M', 'B07NJK86KC', 'B07X4Y7YTD', 'B01MZC86UN', 'B07CZHZQNB', 'B07XRH8VQJ', 'B07CWTZVHV', 'B07W4RBP1C', 'B01A89OWHY', 'B07JP56R7R', 'B07TYPTSTM', 'B07GR5DF45', 'B07NQH4313', 'B01BC6LBGM', 'B01BC6CYK4', 'B01BC6HE6I', 'B01BC6YBGE', 'B01BC7KRWA', 'B06XYT4ZBP', 'B078W3XD6R', 'B07PWN2CYZ', 'B07W5VV6GT', 'B07NQJ61PK', 'B07XS41KX4', 'B077ZJX5W6', 'B07VTP2ZY1', 'B07BK678WN', 'B07WLT5T5P', 'B071CMHW33', 'B075ZTSX5Z', 'B07XX5TT95', 'B07GR5DF45', 'B07SRTF3TJ', 'B00F2GJ3NM', 'B00N3KF15S', 'B0171MA0U4', 'B07CRJJ93S', 'B07KKRT131', 'B07NJK86KC', 'B08238XFF2', 'B0786PQZPW', 'B07VF5ZB7Z', 'B07XS3GWDQ', 'B07XS4MKLF', 'B06XCMVZBS', 'B06XPCD87P', 'B07K6XRB4F', 'B0716ZHJRY', 'B07CZJWW9V', 'B07NQKCH4D', 'B07FZXS14Q', 'B07TTCK5CX', 'B07118K3RJ', 'B0754BXDLG', 'B07NQDTGF8', 'B07PVZR6TW', 'B07XRH8L9Y', 'B075ZSXXTN', 'B07MXZ4KDM', 'B08286YPGW', 'B07C98WHHM', 'B07C98WHHM', 'B082396FPD', 'B0796T6D49', 'B07KKRT131', 'B07NBDDH73', 'B07SZW944C', 'B07TTCLLX3', 'B07W5VTSBG', 'B07C98WHHM', 'B07T6NVXX1', 'B0168RQX40', 'B07B2SL53M', 'B07G5ZW6KN', 'B07TTCMPG6', 'B07X1QXGX1', 'B00F2GJ3NM', 'B079Z2G87Z', 'B07NQH4313', 'B07RCLBQ2P',
# 'B07XS2SN44', 'B07X5V4DL1', 'B07X4Y7YTD', 'B0716ZHJRY', 'B07XLC41DF', 'B0716ZHJRY', 'B00JJH32Z0', 'B07YFX6V6M', 'B073BRD2BT', 'B07BSH63KT', 'B084GT7W7V', 'B07YFZJWB7', 'B07W93N9TR', 'B009UORBV8', 'B06Y526JKK', 'B00JJH32Z0', 'B07BPZTW2Z', 'B00A0ITZBW', 'B00JJH603Q', 'B07BSH63KT', 'B07YFX6V6M', 'B07NJK86KC', 'B07X4Y7YTD', 'B01MZC86UN', 'B07CZHZQNB', 'B07XRH8VQJ', 'B07CWTZVHV', 'B07W4RBP1C', 'B01A89OWHY', 'B07JP56R7R', 'B07TYPTSTM', 'B07GR5DF45', 'B07NQH4313', 'B01BC6LBGM', 'B01BC6CYK4', 'B01BC6HE6I', 'B01BC6YBGE', 'B01BC7KRWA', 'B06XYT4ZBP', 'B078W3XD6R', 'B07PWN2CYZ', 'B07W5VV6GT', 'B07NQJ61PK', 'B07XS41KX4', 'B077ZJX5W6', 'B07VTP2ZY1', 'B07BK678WN', 'B07WLT5T5P', 'B071CMHW33', 'B075ZTSX5Z', 'B07XX5TT95', 'B07GR5DF45', 'B07SRTF3TJ', 'B00F2GJ3NM', 'B00N3KF15S', 'B0171MA0U4', 'B07CRJJ93S', 'B07KKRT131', 'B07NJK86KC', 'B08238XFF2', 'B0786PQZPW', 'B07VF5ZB7Z', 'B07XS3GWDQ', 'B07XS4MKLF', 'B06XCMVZBS', 'B06XPCD87P', 'B07K6XRB4F', 'B0716ZHJRY', 'B07CZJWW9V', 'B07NQKCH4D', 'B07FZXS14Q', 'B07TTCK5CX', 'B07118K3RJ', 'B0754BXDLG', 'B07NQDTGF8', 'B07PVZR6TW', 'B07XRH8L9Y', 'B075ZSXXTN', 'B07MXZ4KDM', 'B08286YPGW', 'B07C98WHHM', 'B07C98WHHM', 'B082396FPD', 'B0796T6D49', 'B07KKRT131', 'B07NBDDH73', 'B07SZW944C', 'B07TTCLLX3', 'B07W5VTSBG', 'B07C98WHHM', 'B07T6NVXX1', 'B0168RQX40', 'B07B2SL53M', 'B07G5ZW6KN', 'B07TTCMPG6', 'B07X1QXGX1', 'B00F2GJ3NM', 'B079Z2G87Z', 'B07NQH4313', 'B07RCLBQ2P',
# 'B07XS2SN44', 'B07X5V4DL1', 'B07X4Y7YTD', 'B0716ZHJRY', 'B07XLC41DF', 'B0716ZHJRY', 'B00JJH32Z0', 'B07YFX6V6M', 'B073BRD2BT', 'B07BSH63KT', 'B084GT7W7V', 'B07YFZJWB7', 'B07W93N9TR', 'B009UORBV8', 'B06Y526JKK', 'B00JJH32Z0', 'B07BPZTW2Z', 'B00A0ITZBW', 'B00JJH603Q', 'B07BSH63KT', 'B07YFX6V6M', 'B07NJK86KC', 'B07X4Y7YTD', 'B01MZC86UN', 'B07CZHZQNB', 'B07XRH8VQJ', 'B07CWTZVHV', 'B07W4RBP1C', 'B01A89OWHY', 'B07JP56R7R', 'B07TYPTSTM', 'B07GR5DF45', 'B07NQH4313', 'B01BC6LBGM', 'B01BC6CYK4', 'B01BC6HE6I', 'B01BC6YBGE', 'B01BC7KRWA', 'B06XYT4ZBP', 'B078W3XD6R', 'B07PWN2CYZ', 'B07W5VV6GT', 'B07NQJ61PK', 'B07XS41KX4', 'B077ZJX5W6', 'B07VTP2ZY1', 'B07BK678WN', 'B07WLT5T5P', 'B071CMHW33', 'B075ZTSX5Z', 'B07XX5TT95', 'B07GR5DF45', 'B07SRTF3TJ', 'B00F2GJ3NM', 'B00N3KF15S', 'B0171MA0U4', 'B07CRJJ93S', 'B07KKRT131', 'B07NJK86KC', 'B08238XFF2', 'B0786PQZPW', 'B07VF5ZB7Z', 'B07XS3GWDQ', 'B07XS4MKLF', 'B06XCMVZBS', 'B06XPCD87P', 'B07K6XRB4F', 'B0716ZHJRY', 'B07CZJWW9V', 'B07NQKCH4D', 'B07FZXS14Q', 'B07TTCK5CX', 'B07118K3RJ', 'B0754BXDLG', 'B07NQDTGF8', 'B07PVZR6TW', 'B07XRH8L9Y', 'B075ZSXXTN', 'B07MXZ4KDM', 'B08286YPGW', 'B07C98WHHM', 'B07C98WHHM', 'B082396FPD', 'B0796T6D49', 'B07KKRT131', 'B07NBDDH73', 'B07SZW944C', 'B07TTCLLX3', 'B07W5VTSBG', 'B07C98WHHM', 'B07T6NVXX1', 'B0168RQX40', 'B07B2SL53M', 'B07G5ZW6KN', 'B07TTCMPG6', 'B07X1QXGX1', 'B00F2GJ3NM', 'B079Z2G87Z', 'B07NQH4313', 'B07RCLBQ2P']
# print(ids)
# print(ids[0:100])
names = product['Item Name'].tolist()

for i in ids:
    a_dict[i] = ""
# print(a_dict)    
# print(names)
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36'
    }    
    # , columns= ['urls']
# searchProducts = product['products'].tolist()

# url = "https://www.amazon.in/Nivia-Shining-Star-2022-Football-White/dp/B00363WZY2"

# @jit(nopython = True)

def scrapyingImages(url,Type,ID):
    global a_dict
    driver = webdriver.Chrome(r'C:\chromedriver\chromedriver.exe',chrome_options=options)
    
    driver.get(url) 
            # this is just to ensure that the page is loaded
            
    # time.sleep(2)
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
        
        # table.write(row, 3, img_src)
        a_dict[ID] = img_src

        # resultImagesList.append(img_src) 
    else:
        img_src = []
        images = soup.find('div',{
            'class': "maintain-height"
        })

        # print(images.img,'jjdadjabaabdbjdbajabsjssjasjssjs')
        # if(images!= None):
        # #     imgList.append(i.img) 
        #     for y in images:
        #         m = str(y['src']) + ','
        #         print(m)
        #         img_src.append(m)
        val = images.img['src'] + ','
        # table.write(row, 3, val)
        a_dict[ID] = val

        # resultImagesList.append(val)  
            


print(len(ids))
# f = requests.get(url, headers = headers,allow_redirects=False)
# print(f)

# 'html.parser'
# @jit(nopython = True)
def mainFunction(ID):
    global a_dict
    Type = type(ID)
    URL = 'https://www.amazon.in/s?k=' + str(ID)
    # f = requests.get(URL, headers = headers,allow_redirects=False)

    # soup = BeautifulSoup(f.content, 'lxml')

    # anchorLink = soup.find('a',{'class': 
    # 'a-link-normal s-no-outline'})
    # print(anchorLink)
    driver = webdriver.Chrome(r'C:\chromedriver.exe',chrome_options=options)
    driver.get(URL)
            # this is just to ensure that the page is loaded
            
    # time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.close()
    anchorLink = soup.find('a',{'class': 
    'a-link-normal s-no-outline'})
    
    if(anchorLink!=None):
        val = 'https://www.amazon.in' + str(anchorLink['href'])
        # resultImages = scrapyingImages(val,Type)
        threading.Thread(target=scrapyingImages,args=(val,Type,ID)).start()

        # return resultImages
    else:
        a_dict[ID] = 'NotFound'
        # resultImagesList.append('NotFound') 

    # soup = BeautifulSoup(f.content, 'lxml')
    # images = soup.find_all('span',{
    #     'class':'a-button-text'
    # })
    # soup = BeautifulSoup(html, 'html.parser')
    

    
row = 1
t1 = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor(20) as executor:
    executor.map(mainFunction,ids)

# def mainthread():

#     for i in range(len(ids)):
#         if(i<19):
#             ID = ids[i]
#             val = type(ID)
#             print(ID,i)
#             # mainFunction(ID,val)
#             threading.Thread(target=mainFunction,args=(ID,val)).start()

# mt = threading.Thread(target=mainthread)
# mt.start()
# mt.join()
time.sleep(5)
for my in range(len(ids)):
    # if(my<19):
    Id = str(ids[my])
    v1 = Id
    v2 = names[my]
    v3 = a_dict.get(Id)
    print(v3,'my')
    table.write(row, 0, my)
    table.write(row, 1, v1)
    table.write(row, 2, v2)  
    table.write(row, 3, v3)

    row+=1 
# Kitchen 12k 17 Feb-scrapying-data4
workbook.save('data-Home.xls')
t2 = time.perf_counter()
print(t2-t1)
print('ok..')   










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
