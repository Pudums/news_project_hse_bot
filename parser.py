import requests
from bs4 import BeautifulSoup

site = "https://medium.com"

def get_themes():
    link = site + "/"
    
    response = requests.get(link).text
    soup = BeautifulSoup(response, "lxml")

    ardo = soup.find("div", attrs={"class":
        "ar do"})

    smth0 = ardo.find("div", attrs={"class":
        "eu af ih ii ij"})

    smth1 = smth0.find("div", attrs={"class":
        "l m n o p q"})

    smth2 = smth1.find("div", attrs={"class":
        "f v s w u"})

    #smth3 = smth2.find("div", attrs={"class":
        #"af"})

    blocs = smth2.find_all("a", attrs={"class":
        "bd be bf bg bh bi bj bk bl bm bn bo bp bq br"})
    return blocs
    

def get_topics(theme):
    link = site + "/topic/" + theme

    if(theme[:4] == "http"):
        link = theme
    
    try:
        response = requests.get(link).text
        soup = BeautifulSoup(response, "lxml")

        blocs = soup.find_all("section")

        res = []
        for i in range(1, 4):
            res.append(blocs[2 * i - 1].find("a"))

        return res
    except:
        return False

def get_name(theme):
    return theme.text

def get_tag(theme):
    link = theme.get("href")
    link = link[link.rfind('/')+1:link.find('?')]
    return link

def get_link(bloc):
    #print(bloc)
    lk = bloc.get("href")
    return (site if lk[0] == '/' else '') \
            + bloc.get("href")

def get_href(bloc):
    return '<a href="' + get_link(bloc) + '">' + bloc.text + "</a>"

def main():
    tops = get_topics("mathfjdla")
    if not tops:
        print(False)
    else:
        print(get_link(tops[0]))

    themes = get_themes()
    print(get_name(themes[0]))
    print(get_tag(themes[0]))

if __name__ == '__main__':
    main()

