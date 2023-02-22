#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
#pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import configparser
import os
import src.pdf_filter as pdf_filter
import datetime
import logging

def crawl_and_download():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)

    dir_main = os.path.dirname(os.path.realpath(__file__))

    dir_path = dir_main + '\output\\'
    dir_path = rf"{dir_path}"

    prefs = {'download.default_directory' : dir_path}
    options.add_experimental_option('prefs', prefs)
    
    #for raspberry pi server config:
    #sudo apt purge --remove chromium-browser -y
    #sudo apt autoremove && sudo apt autoclean -y
    #sudo apt install chromium-chromedriver
    #driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    url = "https://www.ajpes.si/eObjave/default.asp?s=51"
    driver.get(url)

    config = configparser.ConfigParser()
    config.readfp(open(rf'{dir_main}\config.txt'))
    delay = config.get('delay', 'delay')

    #SKUPINA PROCESNEGA DEJANJA = druga procesna dejanja v glavnem postopku
    select = Select(driver.find_element(By.ID, "id_SkupinaVrsta"))
    select.select_by_visible_text("druga procesna dejanja v glavnem postopku")

    #TIP PROCESNEGA DEJANJA = razpis dražbe / vabila k dajanju ponudb
    select = Select(driver.find_element(By.ID, "id_skupinaPodVrsta"))
    select.select_by_visible_text("razpis dražbe / vabila k dajanju ponudb")

    #server config - automatic date
    #today = datetime.date.today().strftime("%d.%m.%Y") #d2
    #yesterday = today - datetime.timedelta(days = 1).strftime("%d.%m.%Y") #d1
    
    d1 = config.get('date', 'd1')
    d2 = config.get('date', 'd2')

    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section[2]/div/form/div[1]/div[1]/div/div[12]/div/div[1]/div/input"))).send_keys(d1)
    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section[2]/div/form/div[1]/div[1]/div/div[12]/div/div[2]/div/input"))).send_keys(d2)

    #select maximum number of results per page
    select = Select(driver.find_element(By.ID, "MAXREC"))
    select.select_by_visible_text("100 zadetkov na stran")

    #look for and click confirm button to trigger search
    isci_gumb = "/html/body/main/section[2]/div/form/div[1]/div[1]/div/div[14]/button[2]"
    element = driver.find_element(By.XPATH, isci_gumb)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section[2]/div/form/div[1]/div[1]/div/div[14]/button[2]"))).click()

    #check if search was triggered
    if "Rezultati iskanja" in driver.page_source:
        next_page = True
    else:
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section[2]/div/form/div[1]/div[1]/div/div[14]/button[2]"))).click()

    if not next_page:
        print("Unable to progress. Exiting...")
        exit()
    #------------------------------------------------------------
    
    hlink_text = "razpis dražbe / vabila k dajanju ponudb"
    seznam_linkov =  []
    seznam_strani = []

    x = "/html/body/main/section[2]/div/div[3]/div/ul/li[1]/a"

    #check how many pages of results there are and add them to list for later looping
    for nr in range(2, 101):
        xpath_full = f'/html/body/main/section[2]/div/div[3]/div/ul/li[{nr}]/a'
        xpath_found = len(driver.find_elements(By.XPATH, xpath_full))

        if xpath_found > 0:
            seznam_strani.append(xpath_full)

    #first page
    seznam_linkov_txt = driver.find_elements(By.LINK_TEXT, hlink_text)
    seznam_linkov += [elem.get_attribute('href') for elem in seznam_linkov_txt]

    #all other pages
    for stran in seznam_strani:
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, stran))).click()
        seznam_linkov_txt = driver.find_elements(By.LINK_TEXT, hlink_text)
        seznam_linkov += [elem.get_attribute('href') for elem in seznam_linkov_txt]

    #----------------------------------------------------------------------------------------
    dl_link_text = "Vsebina procesnega dejanja"

    #download all collected pdfs via url clicking
    for link in seznam_linkov:
        driver.get(link)
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.LINK_TEXT, dl_link_text))).click()

    downloading = True
    while downloading:
        downloading = False
        for file in os.listdir(dir_path):
            if file.endswith('.crdownload'):
                downloading = True
        
    print("All files downloaded...")
    #driver.quit()

if __name__ == '__main__':
    logging.basicConfig(filename = 'file.log',
        level = logging.DEBUG,
        format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    crawl_and_download()

    #filter all downloaded pdfs by specific keywords
    pdf_filter.pdf_filter()
    

