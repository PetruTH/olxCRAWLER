from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import queue

coada = queue.Queue()
lv = []
baseURL = "https://www.olx.ro/imobiliare/?page="

browser = RoboBrowser(parser="html5lib")
browser.open(baseURL)

htmlpage = str(browser.parsed)
bsoup = BeautifulSoup(htmlpage, "html5lib")

pag = bsoup.find_all("a", {"class": "block br3 brc8 large tdnone lheight24"})
nrpag = pag[-1].find("span")
nrpagmax = nrpag.text

i = 0

while i <= int(nrpagmax):
    URL = baseURL + str(i)

    browser = RoboBrowser(parser = "html5lib")
    browser.open(URL)

    htmlpage = str(browser.parsed)
    bsoup = BeautifulSoup(htmlpage, "html5lib")

    anunturi = bsoup.find_all("tr", {"class" : "wrap"})

    for anunt in anunturi:
        for link in anunt.find_all('a'):
            linkurl = link.get('href')
            if linkurl not in lv:
                coada.put(linkurl)
                lv.append(linkurl)
    i+=1

for x in lv:
    print(x)