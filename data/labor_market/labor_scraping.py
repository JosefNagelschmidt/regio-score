# importing packages
from selenium import webdriver
from selenium.webdriver.common.by import By
import geckodriver_autoinstaller
from selenium.webdriver.support import expected_conditions as EC
import json
import datetime
import locale
import time
import os, sys
import pandas as pd 
import re

from functools import partial
from fuzzywuzzy import fuzz

from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait

def getDownLoadedFileName(waitTime):
    driver.execute_script("window.open()")
    WebDriverWait(driver,10).until(EC.new_window_is_opened)
    driver.switch_to.window(driver.window_handles[-1])
    driver.get("about:downloads")

    endTime = time.time()+waitTime
    while True:
        try:
            fileName = driver.execute_script("return document.querySelector('#contentAreaDownloadsView .downloadMainArea .downloadContainer description:nth-of-type(1)').value")
            if fileName:
                return fileName
        except:
            pass
        time.sleep(1)
        if time.time() > endTime:
            break

geckodriver_autoinstaller.install()
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 

# To prevent download dialog
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/Users/light/Documents/Code/Git/regio-score/data/labor_market')
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

##options = Options()
##options.add_argument('--headless')

#driver = webdriver.Firefox(profile)


# setting scrapping range
lower = 2
upper = 3
# upper = 28
# looping over subpages of the website (718 pages) in folds

def get_items(j):
  driver.find_element_by_css_selector("#content > div > div.searchresult > div:nth-child(" + str(j) + ") > div > a").click()
  latestDownloadedFileName = getDownLoadedFileName(5)

  # Source file path 
  source = '/Users/light/Documents/Code/Git/regio-score/data/labor_market/' + str(latestDownloadedFileName)
  renamed_source = '/Users/light/Documents/Code/Git/regio-score/data/labor_market/' + str(page) + "_" + str(j) + ".xlsx"
  os.rename(source, renamed_source) 

  # get destination file name from within the document itself, which is the regional_code:
  id_value = pd.read_excel(io = renamed_source, 
                            header = None,
                            sheet_name = 'Inhaltsverzeichnis', 
                            usecols = [0],
                            nrows = 2,
                            skiprows=[0,1,2,3,4,5,6],
                          engine="openpyxl")
  
  regional_code = re.sub('[()]', '', id_value.iloc[0][0]).split()[-1]

  dest = '/Users/light/Documents/Code/Git/regio-score/data/labor_market/March_2020/' + regional_code + '.xlsx'
  
  driver.close()
  time.sleep(4)
  driver.switch_to.window(driver.window_handles[0])
  os.rename(renamed_source, dest) 
  print(regional_code)


for page in range(lower, upper+1):
  #driver = webdriver.Firefox(firefox_profile= profile, options=options)
  driver = webdriver.Firefox(firefox_profile= profile)
  driver.implicitly_wait(10)

  page_str = str(page) 
  try:  	   
    driver.get('https://statistik.arbeitsagentur.de/SiteGlobals/Forms/Suche/Einzelheftsuche_Formular.html?gtp=15084_list%253D' + page_str + '&topic_f=beschaeftigung-reg-bst-reg')
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[1]/div/div/div/div[3]/button[1]').click()
  except:
    print("This page is missing: " + page_str)
    continue

# each page consists of 20 files
  if page != upper:
    for j in range(19, 21):
      get_items(j = j)
  elif page == upper:
    for j in range(1, 15):
      get_items(j = j)

  driver.close()
