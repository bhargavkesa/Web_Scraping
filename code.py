import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://www.fallingrain.com/world/IN/'

res = requests.get(url)

soup = BeautifulSoup(res.content,'lxml')

link1 = soup.find('ul')
link2 = link1.find_all('li')
links = []


for link in link2:
    links.append(url[:26] + link.a['href'])
    
links = links[2:]
    
def get_response(url):
    flag = 0
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'lxml')
    a_tag = soup.find_all('a')
    links = []
    for link in a_tag:
        if '/world/IN' in link['href']:
            links.append('http://www.fallingrain.com'+link['href'])
    if('.html' in links[0]):
        flag = 1
    
    return links, flag

data = []

while(len(links)>0):
    t_links, flag = get_response(links[-1])
    if flag == 1:
        res = requests.get(links[-1])
        soup = BeautifulSoup(res.content,'lxml')

        table = soup.find('table')
        tr = table.find_all('tr')

        for t_r in tr[1:]:
            tds = t_r.find_all('td')
            temp = [tds[0].text,tds[2].text,tds[4].text,tds[5].text,tds[6].text,tds[7].text]
            print(temp)
            data.append(temp)
        del links[-1]
    else:
        del links[-1]
        for l in t_links:
            if('.html' not in l):
                links.append(l)
        
        
df = pd.DataFrame(data[::-1])
to_csv = df.to_csv('data.csv',header=['City','Region','Latitude', 'Longitude', 'Elevation (in feet)', 'Estimated Population'],index=False)  
        
