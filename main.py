from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time

start = time.time()

lv = []
baseURL = "https://www.olx.ro/imobiliare/?page="

nrpagmax = 0
def find_maxPage():
    browser = RoboBrowser(parser="html5lib")
    browser.open(baseURL)

    htmlpage = str(browser.parsed)
    bsoup = BeautifulSoup(htmlpage, "html5lib")

    pag = bsoup.find_all("a", {"class": "block br3 brc8 large tdnone lheight24"})
    nrpag = pag[-1].find("span")
    nrpagmax = nrpag.text
#nrpagmax sa stiu pe cate pagini sa merg

def generate():
    find_maxPage()
    i = 0
    while i <= 25:
        URL = baseURL + str(i)

        browser = RoboBrowser(parser = "html5lib")
        browser.open(URL)

        htmlpage = str(browser.parsed)
        bsoup = BeautifulSoup(htmlpage, "html5lib")

        anunturi = bsoup.find_all("tr", {"class" : "wrap"})

        for anunt in anunturi:
            for link in anunt.find_all('a'):
                x = link.get('href')
                if x not in lv:
                    lv.append(x)
        i+=1

def scrape_anunt(x):
        if (x[:5] == "https"):
            if (str(x[12] + x[13] + x[14]) == "sto"):  # pt anunturile de pe storia
                print(x)
                anunt = RoboBrowser(parser="html5lib")
                anunt.open(x)

                htmlpage = str(anunt.parsed)
                bsoup = BeautifulSoup(htmlpage, "html5lib")
                header = bsoup.title.text
                filtru = bsoup.find_all("div", {"class": "css-1ccovha estckra9"})  # filtru + valoarea filtru

                if bsoup.find("div", {"data-cy": "adPageAdDescription"}):
                    descriere = bsoup.find("div", {"data-cy": "adPageAdDescription"}).text
                else:
                    descriere = ""
                STORIAtuplu_de_verificat = (header, filtru, descriere)
            else:
                print(x)
                # pt anunturile de pe olx
                anunt = RoboBrowser(parser="html5lib")
                anunt.open(x)
                htmlpage = str(anunt.parsed)
                bsoup = BeautifulSoup(htmlpage, "html5lib")
                if bsoup.title:
                    header = bsoup.title.text
                else:
                    header = ""
                filtre_site = bsoup.find_all("ul", {"class": "css-sfcl1s"})
                if bsoup.find("div", {"class": "css-g5mtbi-Text"}):
                    descriere = bsoup.find("div", {"class": "css-g5mtbi-Text"}).text
                else:
                    descriere = ""
                OLXtuplu_de_verificat = (header, filtre_site, descriere)

#MAIN

if __name__ == '__main__':
    generate()
    # for x in lv:
    #     scrape_anunt(x)
    p = Pool(10)
    link_list = p.map(scrape_anunt, lv)
    p.terminate()
    p.join()
    print(time.time()-start)