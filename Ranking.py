# from elice_utils import EliceUtils  ## 엘리스
import urllib.request
from bs4 import BeautifulSoup

from Crawl_Movie_Ranking import *  # 랭킹크롤링 임포트

# elice_utils = EliceUtils()  # 엘리스


def Ranking(title_list,title_url_list):
    ranking = [('실시간 영화 랭킹 (클릭시 웹페이지로 이동) \n')]

    for i in range(0,10):
        ranking.append(str(i + 1) + "위 : "+"<"+ title_url_list[i] + "|" + title_list[i] +">" + "\n")

    return ranking