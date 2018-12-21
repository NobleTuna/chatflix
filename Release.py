# from elice_utils import EliceUtils  ## 엘리스
import urllib.request
from bs4 import BeautifulSoup
import re

from Crawl_Movie_Ranking import *  # 랭킹크롤링 임포트

# elice_utils = EliceUtils()  # 엘리스


def Release():
    release_list = []
    result_list = []
    result = []
    date_list = []

    url = 'https://movie.naver.com/movie/running/premovie.nhn'

    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")  # 페이지 크롤 soup에 저장

    release_list = soup.find_all("dt", class_="tit")  # 저장, 리스트

    date_list = soup.find_all("span", class_="split") #날짜 입력

    print("여기여기")
    print(date_list)

    for title in release_list:
        result_list.append(title.get_text().strip())  # 문자열 추출(관람등급\n 포함)

    # ['15세 관람가\n더 파티', '전체 관람가\n이차크의 행복한 바이올린', '15세 관람가\n메리 셸리: 프랑켄슈타인의 탄생',
    result_list = result_list[0:11]

    for i in range(0, 11):
        result_list[i] = ((
            result_list[i].replace('전체 관람가\n', '').replace('12세 관람가\n', '').replace('15세 관람가\n', '').replace(
                '청소년 관람불가\n', '')))

    result2 = ['개봉예정작(빠른순)']
    for i in range(10):
        result2.append(str(i + 1) + "위 : " + result_list[i])

    # print(result2)

    return result2