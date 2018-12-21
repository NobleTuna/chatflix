import json
import os
import re
import urllib.request
from bs4 import BeautifulSoup

def img_link(link): ###link 영화 기본 사이트 주소
   # link = "https://movie.naver.com/movie/bi/mi/basic.nhn?code=157297"
   text_image = []
   source_image = urllib.request.urlopen(link).read()
   soup_image = BeautifulSoup(source_image, "html.parser")

   for image in soup_image.find_all("div", class_="poster"):
       text_image.append(image.find("img")["src"])
   # print(text_image[0])
   return str(text_image[0])    ## 이미지 주소 리턴





