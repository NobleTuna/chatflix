# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template
from Crawl_Movie_Ranking import *
from Info import *
from Ranking import *
from Release import *
from Switch import *
from image import *

app = Flask(__name__)

slack_token = ''
slack_client_id = ''
slack_client_secret = ''
slack_verification = ''
sc = SlackClient(slack_token)

title_list = []  # 영화제목 리스트
title_url_list = []  # 영화 제목 주소 리스트

grade = []  # 영화 평점 받아올 리스트
story = []  # 영화 줄거리 받아올 리스트
review = []  # 영화 리뷰 받아올 리스트

global title_URL  # 선택한 영화 주소

global temp22

temp22 = "https://dispatch.cdnser.be/wp-content/uploads/2018/04/20180410162922_28430063_188843508382637_3514609031517831168_n.jpg"


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])


    msg = {}
    keywords =""
    msg["color"] = "#3AA3E3"
    msg["text"] = ""
    msg["image_url"] = "None"



    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]  #text가 실제입력값

        result = re.sub(r'<@\S+> ', '', text)  # result = 받은 텍스트

        title_list, title_url_list = crawl_movie_rank()  # 영화 랭킹페이지 크롤링 호출

        if "순위"  in result:  # 출력 선택 구문
            msg["text"] = str(u'\n'.join(Ranking(title_list,title_url_list)))
        elif "ㅅㅇ"  in result:  # 출력 선택 구문
            msg["text"] = str(u'\n'.join(Ranking(title_list, title_url_list)))
        elif "ㄹㅋ"  in result:  # 출력 선택 구문
            msg["text"] = str(u'\n'.join(Ranking(title_list, title_url_list)))
        elif "ㅇㅈ" in result:
            msg["text"] = str(u'\n'.join(Release()))
        elif "개봉예정작" in result:
            msg["text"] = str(u'\n'.join(Release()))
        elif switching(result, title_list, title_url_list) == "정답":
            for i in range(10):  # 타이틀 리스트 10개를 돌면서 텍스트와 비교해 주소를 url에 넘김, 영화제목이 없으면 url은 비어있음
                if result == title_list[i]:
                    title_URL = title_url_list[i]  # 크롤링할 url 저장한 string
                    break

            msg["image_url"] = img_link(title_URL)
            msg["text"] = str(u'\n'.join(info(title_URL)))  # (영화제목과 주소4)개
        elif "안녕" in result:
            msg["text"] = str(u"안녕하세요")
        # elif "출력실험" in result:
        #     return
        elif "" in result:
            msg["text"] = str("실행 가능 명령어는 아래와 같습니다.\n순위\n개봉예정작\n영화제목(순위권 내)")

        # keywords = answer(text)
        sc.api_call(
                "chat.postMessage",
                channel=channel,
                text=keywords,
                attachments=json.dumps([msg])
            )
        msg["image_url"] = "None"

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000)
