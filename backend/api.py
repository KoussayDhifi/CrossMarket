from fastapi import FastAPI
from bs4 import BeautifulSoup
import re
import requests

app = FastAPI()

mytekURL = "https://www.mytek.tn/catalogsearch/result/index/?product_list_order=price&q="
tunisianetURL = "https://www.tunisianet.com.tn/recherche?controller=search&orderby=price&orderway=asc&s="
jumiaURL = "https://www.jumia.com.tn/catalog/?q="
jumiaURLSuffix = "&sort=lowest-price#catalog-listing"





@app.get("/{article}")
def home(article:str):
    #Fixing the article string
    article = article.strip()
    article = article.replace(" ", "+")
    
    #Getting pages
    mytek = requests.get(mytekURL+article)
    tunisanet = requests.get(tunisianetURL+article)
    jumia = requests.get(jumiaURL+article+jumiaURLSuffix)

    #Getting HTML pages
    mytek = mytek.text
    tunisanet = tunisanet.text
    jumia = jumia.text

    #Giving them to beutifulSoup
    mytek = BeautifulSoup(mytek,"html.parser")
    tunisanet = BeautifulSoup(tunisanet,"html.parser")
    jumia = BeautifulSoup(jumia,"html.parser")
    
    try:
        photosMytek = mytek.find_all("img",class_="product-image-photo",limit=5)
    
        photosMytek = [str(aa['src']) for aa in photosMytek]
        titleMytek = mytek.find_all("a",class_="product-item-link",limit=5)
        linkMytek = [str(aa['href']) for aa in titleMytek]
        titleMytek = [str(aa.contents[0]) for aa in titleMytek]
        pricesMytek = mytek.find_all("span",id=re.compile("^[p][r][o][d][u][c][t][\-][p][r][i][c][e][\-].*$"),limit=5)
        pricesMytek = [str(aa.contents[0].contents[0]) for aa in pricesMytek]
    

        resultMytek = {}
        for i in range(5):
            resultMytek[i] = {
                    "photo":photosMytek[i],
                    "title":titleMytek[i],
                    "link":linkMytek[i],
                    "price":pricesMytek[i]
            }

    except Exception:
        resultMytek = {}

    
   
    
    

        


    return resultMytek





