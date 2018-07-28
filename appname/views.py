from django.shortcuts import render
import requests
import bs4
import re
import random

# Create your views here.

def appmain(request):
    #pythonコード
    while True:
        pokemonnum=random.randrange(493)+1 #807まで
        url = "http://www.pokemon.jp/zukan/detail/" + str(pokemonnum) + ".html"
        res = requests.get(url)

        soup = bs4.BeautifulSoup(res.text, "html5lib")

        title = soup.select(".name")[0].getText()
        char = soup.select(".txt")[0].getText()

        '''
        ptype = []
        for ty in soup.find_all("a"):
            if ty.get("href").startswith("/zukan/?type="):
            	ptype.append(ty.get("span").getText())
        type1 = ptype[0]
        '''

        type1 = "ひこう"


        if pokemonnum >= 1 and pokemonnum <= 151:
            location = "カントー地方"
        elif pokemonnum >= 152 and pokemonnum <= 251:
            location = "ジョウト地方"
        elif pokemonnum >= 252 and pokemonnum <= 386:
            location = "ホウエン地方"
        elif pokemonnum >= 387 and pokemonnum <= 493:
            location = "シンオウ地方"
        elif pokemonnum >= 494 and pokemonnum <= 649:
            location = "イッシュ地方"
        elif pokemonnum >= 650 and pokemonnum <= 721:
            location = "カロス地方"
        elif pokemonnum >= 722 and pokemonnum <= 807:
            location = "アローラ地方"

        description = soup.select("#tab1")[0].getText()
        description2 = description.replace(title, '*' * len(title))
        if description != description2:
            break

        #画像の部分
        images = []
        for link in soup.find_all("img"): # imgタグを取得しlinkに格納
            if link.get("src").startswith("/zukan/images"): # imgタグ内の.pngであるsrcタグを取得
            	images.append("http://www.pokemon.jp"+link.get("src")) # imagesリストに格納

        #for target in images: # imagesからtargetに入れる
        target = images[0]
        re = requests.get(target)
        with open('appname/templates/demo/img/' + "pokemon_image.png", 'wb') as f:# imgフォルダに格納
            f.write(re.content) # .contentにて画像データとして書き込む

        return render(request, 'demo/main.html', {
            'answer' : title,
            'descr' : description2,
            'url' : url,
            'hint1' : location,
            'hint2' : char,
            'hint3' : type1,
        })
