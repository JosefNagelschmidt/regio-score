# importing packages
from selenium import webdriver
from selenium.webdriver.common.by import By
import geckodriver_autoinstaller
from selenium.webdriver.support import expected_conditions as EC
import json
import datetime
import locale
import time

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

#options = Options()
#options.add_argument('--headless')

driver = webdriver.Firefox(profile)
driver.implicitly_wait(10)

# setting scrapping range
lower = 1
upper = 2

# looping over subpages of the website (718 pages) in folds
for page in range(lower, upper+1):
  page_str = str(page) 
  try:  	   
    driver.get('https://statistik.arbeitsagentur.de/SiteGlobals/Forms/Suche/Einzelheftsuche_Formular.html?gtp=15084_list%253D1&topic_f=beschaeftigung-reg-bst-reg')
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[1]/div/div/div/div[3]/button[1]').click()
  except:
    print("This page is missing: " + page_str)
    continue

# each page consists of 20 files
  for j in range(1, 2):
    driver.find_element_by_css_selector("#content > div > div.searchresult > div:nth-child(1) > div > a").click()
    latestDownloadedFileName = getDownLoadedFileName(10)
    print(latestDownloadedFileName)
    

lower_str = str(lower)
upper_str = str(upper)

#print(json.dumps(data_frame),  file=open('/Users/light/Documents/Code/Python/data_scraping/data_' + lower_str + '_' + upper_str +'.json', 'w'))
driver.close()

