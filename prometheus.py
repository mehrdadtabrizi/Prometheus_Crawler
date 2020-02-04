from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from collections import OrderedDict
import Prometheus_Parameters as Parameters
from urllib import request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import time
from os import listdir
from os.path import isfile, join

def browser_open():
    driver = webdriver.Firefox(executable_path=Parameters.Firefox_Driver_PATH)
    return driver

def browser_open_url(browser, url) :
    browser.get(url)
    return browser

def get_page_soup(browser):
    res = browser.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(res, 'lxml')
    return soup

def login():
    print("Signing in as Uni Campus User...")
    browser = browser_open()
    browser = browser_open_url(browser,Parameters.login_url)
    checkbox = browser.find_element_by_xpath("//*/div[@id='campus_login_wrap']/form/fieldset/input[@type='checkbox']")
    checkbox.click()


    signin = browser.find_element_by_xpath("//*/div[@id='campus_login_wrap']/form/fieldset/div[@class='submit_button_wrap float-right']")
    signin.click()


    print("Signed in!")
    return browser

def search_for_the_keyword(browser):

    browser = browser_open_url(browser, Parameters.search_url)
    print("Searching for " + Parameters.SEARCH_KEYWORD)
    title = browser.find_element_by_id("search_value_0")
    title.clear()
    title.send_keys(Parameters.SEARCH_KEYWORD)

    dropdownbox = browser.find_element_by_xpath("//*/select[@id='boolean_fields_selected_2']").send_keys("und nicht")

    title_not = browser.find_element_by_id("search_value_2")
    title_not.clear()
    title_not.send_keys(Parameters.NON_RELEVANT_KEYWORD)

    submit = browser.find_element_by_xpath("//*/div[@class='button_wrap submit_button']")
    submit.click()

    return browser

def extract_items_metadata(browser):

    page_odd_items = []
    page_even_items = []
    page_items = []
    page_dic = []
    artist = ' '
    location = ' '
    date = ' '
    title = ' '
    material = ' '
    genre = ' '
    image_url = ' '
    file_name = ' '
    subtitle = ' '
    item_link = ''

    soup = get_page_soup(browser)
    page_number = soup.find('input', {'id': 'page'}).get('placeholder')
    print("Current page: " + page_number)

    try:
        page_odd_items  = soup.find_all('div', {'class' : 'list_row odd undim'})
    except:
        pass
    try:
        page_even_items = soup.find_all('div', {'class': 'list_row even undim'})
    except:
        pass
    if (page_even_items is not None) and (page_odd_items is not None):
        page_items = page_even_items + page_odd_items

    for item in page_items:
        try:
                date = item.find('td' , {'class' : 'date-field'}).text.replace('\n', '').replace('\t', '')

                artist = item.find('td', {'class': 'artist-field'}).text.replace('\n', '').replace('\t', '')
                location = item.find('td' , {'class' : 'location-field'}).text.replace('\n', '').replace('\t', '')
                title = item.find('td' , {'class' : 'title-field'}).text.replace('\n', '').replace('\t', '')
                item_link = Parameters.base_url + item.find('div' , {'class' : 'image'}).find('a').get('href')

                hr = item_link.split('/')[-1]
                image_url = "http://prometheus.uni-koeln.de/pandora/image/large/" + hr

                file_name = hr + '.jpg'

                #download_image(image_url,file_name)

                item_dic = {
                    'Photo Archive': Parameters.base_url,
                    'Iconography' : Parameters.Iconography,
                    'Branch' : 'ArtHist',
                    'File Name': file_name,
                    'Title': title,
                    'Additional Information': subtitle,
                    'Artist': artist,
                    'Earliest Date': date,
                    'Current Location': location,
                    'Genre': genre,
                    'Material': material,
                    'Details URL': item_link,
                    'Image Credits': image_url
                }
                keyorder = Parameters.Header
                item_dic = OrderedDict(sorted(item_dic.items(), key=lambda i: keyorder.index(i[0])))
                page_dic.append(item_dic)
        except:
            pass
    print('Metadatas of page ' + str(page_number) + ' are being appended to csv file.')
    print('......................')
    return page_dic

def go_to_page_number(browser,page_number):

        next_page = browser.find_element_by_xpath("//*/div[@class='pagination']//*/input[@id='page']")
        next_page.clear()
        next_page.send_keys(page_number)
        los       = browser.find_element_by_xpath("//*/div[@class='pagination']//*/div[@class='autosubmit scriptonly']")
        los.click()
        return True

def download_image(url,file_name):
    path = Parameters.Images_PATH + file_name
    request.urlretrieve(url, path)


def create_csv_file(file_path):
    keyorder = Parameters.Header
    with open(file_path, "w") as f:
        wr = csv.DictWriter(f, dialect="excel", fieldnames=keyorder)
        wr.writeheader()


def append_metadata_to_CSV(list):
    keyorder = Parameters.Header
    with open(Parameters.CSV_File_PATH, "a" , encoding="utf-8") as fp:
        wr = csv.DictWriter(fp,dialect="excel",fieldnames=keyorder)
        for dic in list:
            wr.writerow(dic)

def browser_quit(browser):
    browser.quit()
