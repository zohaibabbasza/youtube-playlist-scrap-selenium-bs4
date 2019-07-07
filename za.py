from bs4 import BeautifulSoup as bs
import requests
import csv
from itertools import zip_longest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random

caps = DesiredCapabilities.CHROME


caps["marionette"] = True

geckodriver="./chromedriver"





def scrollDown(browser, numberOfScrollDowns):
    body = browser.find_element_by_tag_name("body")
    while numberOfScrollDowns >=0:
        body.send_keys(Keys.PAGE_DOWN)
        numberOfScrollDowns -= 1
    return browser


def get_link_id(artist):
    #LINK ID HERE

    driver = webdriver.Chrome(geckodriver)
    print("Looking For Playlist")
    driver.get("https://www.youtube.com/results?search_query={0}&sp=EgIQAw%253D%253D".format(artist))
    driver = scrollDown(driver,800)
    time.sleep(5)
    user_data = driver.find_elements_by_xpath('//*[@id="view-more"]/a')
    links = []
    for i in user_data:
                z= i.get_attribute('href').split('list=')
                links.append(z[1])
                

    print("{0} Playlist Found".format(len(links)))
    driver.close()
    return links

def write_to_csv(artist,links,titles):
    d = [titles, links]
    export_data = zip_longest(*d, fillvalue = '')
    with open(artist+'.csv', 'a', encoding="utf-8", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("titles", "links"))
        wr.writerows(export_data)
    myfile.close()
 


def get_url_title(artist):
    list_ids = []
    list_ids = get_link_id(artist)
    print("scraping started....")
    z = 0
    for k in list_ids:
        for_title = 'https://www.youtube.com/watch?v=pRpeEdMmmQ0&list='
        for_url = 'https://www.youtube.com/playlist?list='
        #URL HERE
        r = requests.get(for_url+k)
        page = r.text
        soup=bs(page,'html.parser')
        links=soup.find_all('a',{'class':'pl-video-title-link'})
        #TITLE HERE
        r = requests.get(for_title+k)
        page = r.text
        soup=bs(page,'html.parser')
        h4 = soup.find_all("h4",text=True)
        h4 = h4[:-6]
        titles = []
        link = []
        for l in  range(len(links)):
            try:
                titles.append(h4[l].text)
            except IndexError:
                titles.append('null')
            try:
                link.append('www.youtube.com' + links[l].get('href'))
            except IndexError:
                link.append('null')
        write_to_csv(artist,link,titles)
        time.sleep(random.randint(0,20))
    print("Successfully Done")

def main():
    print("Input Artist Name:")
    artist = input()
    get_url_title(artist)
    #single(artist)

main()