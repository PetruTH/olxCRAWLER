from robobrowser import RoboBrowser
from bs4 import BeautifulSoup

lv = []
baseURL = "https://www.olx.ro/imobiliare/?page="

browser = RoboBrowser(parser="html5lib")
browser.open(baseURL)

htmlpage = str(browser.parsed)
bsoup = BeautifulSoup(htmlpage, "html5lib")

pag = bsoup.find_all("a", {"class": "block br3 brc8 large tdnone lheight24"})
nrpag = pag[-1].find("span")
nrpagmax = nrpag.text
#nrpagmax sa stiu pe cate pagini sa merg

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
            x = link.get('href')
            if x not in lv:
                if (x[:5] == "https"):
                    if (str(x[12] + x[13] + x[14]) == "sto"):  # pt anunturile de pe storia
                        print(x)
                        anunt = RoboBrowser(parser="html5lib")
                        anunt.open(x)

                        htmlpage = str(anunt.parsed)
                        bsoup = BeautifulSoup(htmlpage, "html5lib")

                        header = bsoup.find("h1", {"class": "css-11kn46p eu6swcv17"}).text  # titlu

                        filtru = bsoup.find_all("div", {"class": "css-1ccovha estckra9"})  # filtru + valoarea filtru

                        descriere = bsoup.find("div", {"data-cy": "adPageAdDescription"}).text

                        STORIAtuplu_de_verificat = (header, filtru, descriere)
                    else:
                        print(x)
                        anunt = RoboBrowser(parser="html5lib")
                        anunt.open(x)

                        htmlpage = str(anunt.parsed)
                        bsoup = BeautifulSoup(htmlpage, "html5lib")

                        header = bsoup.title.text
                        filtre_site = bsoup.find_all("ul", {"class": "css-sfcl1s"})
                        if bsoup.find("div", {"class": "css-g5mtbi-Text"}):
                            descriere = bsoup.find("div", {"class": "css-g5mtbi-Text"}).text
                        else:
                            descriere = ""

                        OLXtuplu_de_verificat = (header, filtre_site, descriere)
                lv.append(x)
    i+=1

#formeaza lista de anunturi de pe olx si storia
