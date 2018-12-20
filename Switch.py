# from elice_utils import EliceUtils  ## 엘리스
import urllib.request
from bs4 import BeautifulSoup


def switching(text, title_list, title_url_list):
    url = 'None'  # 다음 for문에서 크롤링할 url 저장할 리스트

    for i in range(10):  # 타이틀 리스트 10개를 돌면서 텍스트와 비교해 주소를 url에 넘김, 영화제목이 없으면 url은 비어있음
        if text == title_list[i]:
            url = title_url_list[i]  # 크롤링할 url 저장한 string
            break
        else:
            pass

    if url == 'None':  # for문이 끝나고 url이 None이면 result에 오류메시지를 보내 리턴
        return '오답'

    else:  # url이 존재하면 정답     #############################

        return '정답'