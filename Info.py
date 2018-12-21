# from elice_utils import EliceUtils
import json
import os
import re
import urllib.request

import urllib.request  # 웹페이지를 여는데 이용하는 모듈
from bs4 import BeautifulSoup  # 크롤링 하는데 이용하는 모듈

# elice_utils = EliceUtils()


def listToStringWithoutBrackets(list1):  ##### 리스트의 대괄호 제거 함수
    return str(list1).replace('[', '').replace(']', '')

def cineprint(txt):
    temp = []
    # print("요기 : "+txt)
    for i in txt: # 01 23 45 67 89
        temp.append(str(i[0]) +" "+ str(i[1]))
    # print("여기부터")
    # print(temp)
    return '\n'.join(temp)

def replyprint(txt):

    return '\n'.join(txt)


def info(url):
    # print("원하시는 정보를 입력하세요")
    # answer = input()
    urlCode = url[-6:]
    ###### basic ->기본 정보 || review -> 평점 || running -> 상영관 ||
    basic_url_start = "https://movie.naver.com/movie/bi/mi/"  ##### 크롤링한 주소 나눠서 사용
    basic_url_end = ".nhn?code=157297"
    ##### url 주소
    url_cine = basic_url_start + "running" + basic_url_end  ##### 상영관 url
    url_story = "https://movie.naver.com/movie/bi/mi/basic.nhn?code=" + urlCode  ##### 줄거리 url
    url_reply = "https://movie.naver.com/movie/bi/mi/review.nhn?code=" + urlCode
    url_star = "https://movie.naver.com/movie/bi/mi/review.nhn?code=" + urlCode

    #     ##### BeautifulSoup -> url
    source_cine = urllib.request.urlopen(url_cine).read()
    soup_cine = BeautifulSoup(source_cine, "html.parser")  ##### 상영관
    source_story = urllib.request.urlopen(url_story).read()
    soup_story = BeautifulSoup(source_story, "html.parser")  ##### 줄거리
    source_reply = urllib.request.urlopen(url_reply).read()
    soup_reply = BeautifulSoup(urllib.request.urlopen(url_reply).read(), "html.parser")
    source_star = urllib.request.urlopen(url_star).read()
    soup_star = BeautifulSoup(urllib.request.urlopen(url_star).read(), "html.parser")

    ##### 크롤링 정보 저장
    text_cine = []
    text_story = []
    text_reply = []
    text_star = []

    answer_cine = ["-------------"]
    answer_story = ["-------------"]
    answer_reply = ["-------------"]
    answer_star = ["-------------"]

    ##### 질문이 상영관(cine)일경우
    # if answer == "cine":
    cine_titles = soup_cine.find_all("p", class_="cine_title")
    for cine in cine_titles:
        text_cine.append(cine.get_text().split()[:2])
    answer_cine.append("\n주변 상영관 \n"+ listToStringWithoutBrackets(cineprint(text_cine)))
    # print(answer_cine)
    # return print("주변 상영관은 " + str(listToStringWithoutBrackets(text_cine)) + "입니다.")

    ##### 질문이 줄거리(story)일경우
    # elif answer == "story":
        ######
    story_titles = soup_story.find_all("p", class_="con_tx")
    for story in story_titles:
        text_story.append(story.get_text().replace("\r\xa0", ""))  ##### \r\xa0--> 네이버에서 줄바꿀때 생김
        text_story = [w.replace('\xa0', ' ') for w in text_story]# 가져온 소스
        text_story = text_story[:1]  #### 1번-> 줄거리 // 2번 제작노트
    answer_story.append(listToStringWithoutBrackets(text_story).replace("'", "")+"\n")
    # return print(listToStringWithoutBrackets(text_story).replace("'", ""))

##### 질문이 댓글(reply)일경우
# elif answer == "reply":
    for reply in soup_reply.find_all("ul", class_="rvw_list_area"):
        for reply2 in reply.find_all("li"):
            for reply3 in reply2.find_all("strong"):#replyprint(txt)
                text_reply.append(reply3.get_text())
    answer_reply.append("관람객 후기\n" + listToStringWithoutBrackets(replyprint(text_reply[:5])))
    # return print("최신 댓글 입니다. \n" + listToStringWithoutBrackets(str(text_reply[:1])))

##### 질문이 별점(star)일경우
# elif answer == "star":
    star_titles = soup_star.find_all("span", class_="st_on")
    for star in star_titles[:1]:
        text_star.append(star.get_text())

    answer_star.append(listToStringWithoutBrackets(text_star).replace("'", "") + "입니다.")
    # return print(listToStringWithoutBrackets(text_star).replace("'", "") + "입니다.")

    # url.append("\n")
    # url = str(url)
    final_result = ["\n<"+ str(url)+"|상세정보보기 클릭!>\n"]  #<http://bar.com|bar>
    # print(type(final_result))
    # print(type(url))
    return answer_star + answer_story + answer_reply + answer_cine + final_result

    ##### 그밖의 경우
    # else:
    #     return print("외국말이야?")

    # URL 주소에 있는 HTML 코드를 soup에 저장합니다.

    # print(text_story)

#
# if __name__ == "__main__":
#     main()
