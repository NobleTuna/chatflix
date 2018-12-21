# from elice_utils import EliceUtils  ## 엘리스
import urllib.request
from bs4 import BeautifulSoup

# elice_utils = EliceUtils()  # 엘리스


def crawl_movie_rank():
    title_list = []
    title_url_list = []

    url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn'

    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")  # 페이지 크롤 soup에 저장

    list_ranking = soup.find_all("div", class_="tit3")  # 검색

    for title in list_ranking:
        title_list.append(title.get_text().strip())
        # title_url_list.append(title.find("a")["href"][-6:])
        title_url_list.append('https://movie.naver.com' + title.find("a")["href"])

    title_list = title_list[0:10]
    title_url_list = title_url_list[0:10]

    # for i range(0,10)
    #     title_list


    # print(title_list)
    # print(title_url_list)

    return (title_list, title_url_list)
