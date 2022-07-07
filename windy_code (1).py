#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 14:06:49 2022

@author: asus
"""
from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

import time

import pandas as pd

from bs4 import BeautifulSoup

from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from random import randrange

import os
def data_extraction (loc):
    from selenium import webdriver

    from selenium.webdriver.common.keys import Keys

    from selenium.webdriver.common.by import By

    import time

    from selenium.webdriver.common.keys import Keys
    import pandas as pd

    from bs4 import BeautifulSoup

    from selenium.webdriver.chrome.service import Service

    from webdriver_manager.chrome import ChromeDriverManager

    from random import randrange

    s=Service(ChromeDriverManager().install())

    #driver = webdriver.Chrome(service=s)
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.maximize_window()
    

    ###########################################

    random_num = randrange(15,25)

    driver.get('https://www.windy.com/28.040/78.790/wind?27.506,78.788,8,m:erTaimu')
    driver.implicitly_wait(10)

    click = driver.find_element(By.XPATH,'//*[@id="login"]').click()

    time.sleep(randrange(15,25))

    login = driver.find_element(By.XPATH,'//*[@id="email"]')

    login.send_keys('ashish.redfx')

    password = driver.find_element(By.XPATH,'//*[@id="password"]')

    password.send_keys('Red@123$')

    password.send_keys(Keys.ENTER)

    location = driver.find_element(By.XPATH,'//*[@id="q"]')

    location.send_keys(loc)

    i = 1
    while i<15:

        location.send_keys(Keys.ENTER)
        i = i+1
    time.sleep(randrange(15,25))
    driver.implicitly_wait(10)
    #location.send_keys(Keys.ENTER)
    driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/div[5]/div[1]').click()

    page_source = driver.page_source

    soup = BeautifulSoup(page_source,'lxml')

    ### DATA EXTRACTION FROM ECW
    time.sleep(random_num)

    p = driver.find_element(By.XPATH,'//*[@id="detail-data-table"]/tbody/tr[3]')

    f = [int(i) for i in p.text.split() if i.isdigit()]
    min_ECW = []

    max_ECW = []

    for i in range(0,len(f)):
        if i%2:
            max_ECW.append(f[i])
        else:
            min_ECW.append(f[i])
    min_ECW,max_ECW

    try :
        f3 = pd.DataFrame(list(zip(min_ECW,max_ECW)),columns = ['Min Speed(m/s)_ECW','Max Speed(m/s)_ECW'])
    except :
        f3= pd.DataFrame()
    ### DATA EXTRACTION FROM GFS

    s = driver.find_element(By.XPATH,'//*[@id="detail-data-table"]/tbody/tr[4]')

    e = [int(i) for i in s.text.split() if i.isdigit()]

    min_GFS = []

    max_GFS = []

    for i in range(0,len(e)):
        if i%2:
            max_GFS.append(e[i])
        else:
            min_GFS.append(e[i])

    min_GFS,max_GFS
    
    try :

        f2 = pd.DataFrame(list(zip(min_GFS,max_GFS)),columns = ['Min Speed(m/s)_GFS','Max Speed(m/s)_GFS'])
    except :
        f2  = pd.DataFrame()
    ### EXTRACTING DATA FROM ICON

    time.sleep(randrange(15,25))

    a = driver.find_element(By.XPATH,'//*[@id="detail-data-table"]/tbody/tr[5]')

    b= [int(i) for i in a.text.split() if i.isdigit()]

    min_ICON = []

    max_ICON = []

    for i in range(0,len(b)):
        if i%2:
            max_GFS.append(b[i])
        else:
            min_GFS.append(b[i])

    min_ICON,max_ICON
    try:

        f4 = pd.DataFrame(list(zip(min_ICON,max_ICON)),columns = ['Min Speed(m/s)_ICON','Max Speed(m/s)_ICON'])
    except :
        f4= pd.DataFrame()
    ### EXTRACTING DATA FROM METEOBLUE

    c = driver.find_element(By.XPATH,'//*[@id="detail-data-table"]/tbody/tr[6]')

    d= [int(i) for i in c.text.split() if i.isdigit()]

    min_MB = []

    max_MB = []

    for i in range(0,len(d)):
        if i%2:
            max_MB.append(d[i])
        else:
            min_MB.append(d[i])

    min_MB,max_MB
    
    try :

        f5 = pd.DataFrame(list(zip(min_MB,max_MB)),columns = ['Min Speed(m/s)_MB','Max Speed(m/s)_MB'])
    except :
        f5= pd.DataFrame()
    time.sleep(random_num)

    ### EXTRACTING TIME DATA

    time = driver.find_element(By.XPATH,'//*[@id="detail-data-table"]/tbody/tr[2]')

    time_split= time.text.split()

    t = pd.DataFrame(time_split)

    ## COMBINING THE FINAL DATAFRAME

    new= []
    for i in range(1,78):
        titles = driver.find_element(By.XPATH,'//*[@id="detail-data-table"]/tbody/tr[2]/td['+str(i)+']').get_attribute("data-ts")
        new.append(titles)
    data = pd.DataFrame(new)

    datatime= pd.to_datetime(data.iloc[:,0],unit = 'ms')

    td = pd.DataFrame(datatime)
    

    df_FINAL = pd.concat([td,f3,f2,f4,f5],axis = 1)

    pd.set_option('display.max_rows' ,78)
    try :
        

        df_FINAL.columns = ['DATATIME','UGRD100M','VGRD100M','T2M','DIR_HI','CLDCVR', 'SURF_PRESSURE', 'WIND_DIR_100M','WIND_SPEED_100M']

    except:
        return pd.DataFrame()
    #df_1 = pd.DataFrame(columns=['CLDCVR', 'SURF_PRESSURE', 'WIND_DIR_100M','WIND_SPEED_100M'])

    #df = pd.concat([df_FINAL,df_1])
    
    return df_FINAL

list_ = ['23.81039,75.06278','23.92733,71.20236']
dataframes=[]
dataframe=pd.DataFrame()
i=0
while i < len(list_):
    print(list_[i])
    time.sleep(randrange(15,25))
    
    dataframe = data_extraction(list_[i])
    
    if len(dataframe)!=0:
        i=i+1
        
    dataframes.append(dataframe)
