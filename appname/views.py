from django.shortcuts import render
import requests
import bs4
import re
import random

# Create your views here.

def appmain(request):
    #pythonコード
    while True:
        num = random.randrange(493)+1 #807まで
        if num < 10:
            pokemonnum = "00" + str(num)
        elif num >= 10 and num < 100:
            pokemonnum = "0" + str(num)
        else:
            pokemonnum = str(num)
        url = "http://www.pokemon.jp/zukan/detail/" + str(pokemonnum) + ".html"
        res = requests.get(url)

        #soup = bs4.BeautifulSoup(res.text, "html5lib")
        soup = bs4.BeautifulSoup(res.text, "html5lib")

        title = soup.select(".name")[0].getText()
        char = soup.select(".txt")[0].getText()


        #タイプ
        cnt = 0
        ptype = []
        type = ""
        for typ in soup.find_all(class_="pokemon-type col2"):
            for typ1 in typ.find_all("li"):
                ptype.append(typ1.get("class"))
                if cnt > 0:
                    type = type + "・"
                type = type + soup.select("." + str(ptype[cnt]).strip('[]\'', ) + " span")[0].getText()
                cnt = cnt + 1
            if cnt > 0:
                break


        if num >= 1 and num <= 151:
            location = "カントー地方"
        elif num >= 152 and num <= 251:
            location = "ジョウト地方"
        elif num >= 252 and num <= 386:
            location = "ホウエン地方"
        elif num >= 387 and num <= 493:
            location = "シンオウ地方"
        elif num >= 494 and num <= 649:
            location = "イッシュ地方"
        elif num >= 650 and num <= 721:
            location = "カロス地方"
        elif num >= 722 and num <= 807:
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

        imgurl = images[0]
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
            'hint3' : type,
            'imgurl' : imgurl,
        })
