from fastapi import FastAPI
from bs4 import BeautifulSoup
import re
import requests

app = FastAPI()

mytekURL = "https://www.mytek.tn/catalogsearch/result/index/?q="
tunisianetURL = "https://www.tunisianet.com.tn/recherche?controller=search&orderby=price&orderway=asc&s="
jumiaURL = "https://www.jumia.com.tn/catalog/?q="


jPriceConv = lambda x : float(x.replace(',','.')[0:x.find('TND')])
MPriceConv = lambda x : float(x.replace(',','.')[0:x.find('DT')])


@app.get("/{article}")
def home(article:str,narticles:int=5):
    #Fixing the article string
    article = article.strip()
    article = article.replace(" ", "+")
    
    #Getting pages
    mytek = requests.get(mytekURL+article)
    tunisanet = requests.get(tunisianetURL+article)
    jumia = requests.get(jumiaURL+article)

    #Getting HTML pages
    mytek = mytek.text
    tunisanet = tunisanet.text
    jumia = jumia.text

    #Giving them to beutifulSoup
    mytek = BeautifulSoup(mytek,"html.parser")
    tunisanet = BeautifulSoup(tunisanet,"html.parser")
    jumia = BeautifulSoup(jumia,"html.parser")
    
    try:
        photosMytek = mytek.find_all("img",class_="product-image-photo",limit=narticles)
        photosMytek = [str(aa['src']) for aa in photosMytek]
        titleMytek = mytek.find_all("a",class_="product-item-link",limit=narticles)
        linkMytek = [str(aa['href']) for aa in titleMytek]
        titleMytek = [str(aa.contents[0]) for aa in titleMytek]
        pricesMytek = mytek.find_all("span",id=re.compile("^[p][r][o][d][u][c][t][\-][p][r][i][c][e][\-].*$"),limit=narticles)
        pricesMytek = [str(aa.contents[0].contents[0]) for aa in pricesMytek]

        mytekitems = list(zip(pricesMytek,titleMytek,linkMytek,photosMytek))
        mytekitems = sorted(mytekitems,key=lambda x:float(x[0].replace(',','.')[0:x[0].find("DT")]))

        pricesMytek,titleMytek,linkMytek,photosMytek = zip(*mytekitems)
        
  

    except Exception:
        pricesMytek,titleMytek,linkMytek,photosMytek = [],[],[],[]

    try:
        photosTunisiaNet = tunisanet.find_all("img",width="250",height="250",limit=narticles)
        photosTunisiaNet = [str(aa['src']) for aa in photosTunisiaNet]
        titlesTunisiaNet = tunisanet.find_all("h2",class_="product-title",limit=narticles)
        titlesTunisiaNet = [aa.contents[0] for aa in titlesTunisiaNet]
        linksTunisiaNet = [str(aa['href']) for aa in titlesTunisiaNet]
        titlesTunisiaNet = [str(aa.contents[0]) for aa in titlesTunisiaNet]
        pricesTunisiaNet = tunisanet.find_all("div",class_="wb-action-block",limit=narticles)
        pricesTunisiaNet = [str(aa.contents[7].contents[1].contents[0]) for aa in pricesTunisiaNet]
        resultTunisiaNet = {}

        TunisiaNetitems = list(zip(pricesTunisiaNet,titlesTunisiaNet,linksTunisiaNet,photosTunisiaNet))
        TunisiaNetitems = sorted(TunisiaNetitems,key=lambda x:float(x[0].replace(',','.')[0:x[0].find("DT")]))

        pricesTunisiaNet,titlesTunisiaNet,linksTunisiaNet,photosTunisiaNet = zip(*TunisiaNetitems)
        
   
    except Exception:
        pricesTunisiaNet,titlesTunisiaNet,linksTunisiaNet,photosTunisiaNet = [],[],[],[]
    
    try:
        photosJumia = jumia.find_all("div",class_="img-c",limit=narticles)
        photosJumia = [str(aa.contents[0]['data-src']) for aa in photosJumia]
        titlesJumia = jumia.find_all(class_="name",limit=narticles)
        titlesJumia = [str(aa.contents[0]) for aa in titlesJumia]
        linksJumia = jumia.find_all("a" ,class_="core", limit=narticles)
        linksJumia = ["https://www.jumia.com.tn"+str(aa['href']) for aa in linksJumia]
        pricesJumia = jumia.find_all(class_="prc", limit=narticles)
        pricesJumia = [str(aa.contents[0]) for aa in pricesJumia]
        

        Jumiaitems = list(zip(pricesJumia,titlesJumia,linksJumia,photosJumia))
        Jumiaitems = sorted(Jumiaitems,key=lambda x:float(x[0].replace(',','.')[0:x[0].find("TND")]))

        pricesJumia,titlesJumia,linksJumia,photosJumia = zip(*Jumiaitems)

    except Exception:
        pricesJumia,titlesJumia,linksJumia,photosJumia = [],[],[],[]

    
    auxPrices = []
    auxPhotos = []
    auxTitles = []
    auxLinks = []

    

    m = 0
    t = 0

    while (m<len(pricesMytek) and t<len(pricesTunisiaNet)):
        if (MPriceConv(pricesMytek[m]) > MPriceConv(pricesTunisiaNet[t])):
            auxPrices.append(pricesTunisiaNet[t])
            auxPhotos.append(photosTunisiaNet[t])
            auxTitles.append(titlesTunisiaNet[t])
            auxLinks.append(linksTunisiaNet[t])
            t+=1
        else:
            auxPrices.append(pricesMytek[m])
            auxPhotos.append(photosMytek[m])
            auxTitles.append(titleMytek[m])
            auxLinks.append(linkMytek[m])
            m+=1

    while (m<len(pricesMytek)):
        auxPrices.append(pricesMytek[m])
        auxPhotos.append(photosMytek[m])
        auxTitles.append(titleMytek[m])
        auxLinks.append(linkMytek[m])
        m+=1
    
    while (t<len(pricesTunisiaNet)):
        auxPrices.append(pricesTunisiaNet[t])
        auxPhotos.append(photosTunisiaNet[t])
        auxTitles.append(titlesTunisiaNet[t])
        auxLinks.append(linksTunisiaNet[t])
        t+=1
    
    finalPrices = []
    finalPhotos = []
    finalTitles = []
    finalLinks = []

    a = 0
    j = 0

    while (a<len(auxPrices) and j<len(pricesJumia)):
        if (MPriceConv(auxPrices[a]) > jPriceConv(pricesJumia[j])):
            finalPrices.append(pricesJumia[j])
            finalPhotos.append(photosJumia[j])
            finalTitles.append(titlesJumia[j])
            finalLinks.append(linksJumia[j])
            j+=1
        else:
            finalPrices.append(auxPrices[a])
            finalPhotos.append(auxPhotos[a])
            finalTitles.append(auxTitles[a])
            finalLinks.append(auxLinks[a])
            a+=1

    while (a<len(auxPrices)):
        finalPrices.append(auxPrices[a])
        finalPhotos.append(auxPhotos[a])
        finalTitles.append(auxTitles[a])
        finalLinks.append(auxLinks[a])
        a+=1

    while (j<len(pricesJumia)):
        finalPrices.append(pricesJumia[j])
        finalPhotos.append(photosJumia[j])
        finalTitles.append(titlesJumia[j])
        finalLinks.append(linksJumia[j])
        j+=1

    finalResult = {}

    for i in range(len(finalTitles)):
        finalResult[i] = {
            "photo":finalPhotos[i],
            "link":finalLinks[i],
            "title":finalTitles[i],
            "price":finalPrices[i]
        }

    return finalResult





