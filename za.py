from bs4 import BeautifulSoup as bs
import requests

def get_link_id(artist):
    #LINK ID HERE
    if " " in artist:
        artist = artist.replace(" ",'+')
        print(artist)
    r = requests.get('https://www.youtube.com/results?search_query={0}&sp=EgIQAw%253D%253D'.format(artist))
    page = r.text
    soup=bs(page,'html.parser')
    za=soup.find_all('a',{'class':'yt-lockup-playlist-item-title yt-uix-sessionlink spf-link'})
    print(len(za))
    i =0
    ids = []  
    while i != len(za):
        z = za[i].get('href').split('list=')
        print(z[1])
        ids.append(z[1])
        i+=2
    return ids


def get_url_title(artist):
    list_ids = []
    list_ids = get_link_id(artist)
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
        print(len(links))
        print(len(h4))
        for l in links:
            print('www.youtube.com' + l.get('href'))
        
        for i in h4:
            print(i.text)


def main():
    print("Input Artist Name:")
    artist = input()
    get_url_title(artist)


main()