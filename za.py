from bs4 import BeautifulSoup as bs
import requests
import csv
from itertools import zip_longest


def get_link_id(artist):
    #LINK ID HERE
    if " " in artist:
        artist = artist.replace(" ",'+')
        print(artist)
    r = requests.get('https://www.youtube.com/results?search_query={0}&sp=EgIQAw%253D%253D'.format(artist))
    page = r.text
    soup=bs(page,'html.parser')
    za=soup.find_all('a',{'class':'yt-lockup-playlist-item-title yt-uix-sessionlink spf-link'})
    i =0
    ids = []  
    while i != len(za):
        z = za[i].get('href').split('list=')
        ids.append(z[1])
        i+=2
    return ids

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
                titles.append(h4[l].text)
            try:
                link.append('www.youtube.com' + links[l].get('href'))
            except IndexError:
                link.append('null')    
        write_to_csv(artist,link,titles)
    print("Successfully Done")

def main():
    print("Input Artist Name:")
    artist = input()
    get_url_title(artist)
    #single(artist)

main()