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

app = Flask(__name__)



title_list = []  # 영화제목 리스트
title_url_list = []  # 영화 제목 주소 리스트

grade = []  # 영화 평점 받아올 리스트
story = []  # 영화 줄거리 받아올 리스트
review = []  # 영화 리뷰 받아올 리스트

title_URL = [] #선택한 영화 주소



def answer(text): #구동부

    result = re.sub(r'<@\S+> ', '', text) # result = 받은 텍스트

    title_list, title_url_list = crawl_movie_rank()  # 영화 랭킹페이지 크롤링 호출


    if "순위" in result:  #출력 선택 구문
        Ranking(title_list)
        return u'\n'.join(title_list)
    elif "개봉예정작" in result:
        return u'\n'.join(Release())
    elif switching(result,title_list,title_url_list) == "정답":
        for i in range(10):  # 타이틀 리스트 10개를 돌면서 텍스트와 비교해 주소를 url에 넘김, 영화제목이 없으면 url은 비어있음
            if result == title_list[i]:
                title_URL = title_url_list[i]  # 크롤링할 url 저장한 string
                break
        return u'\n'.join(info(title_URL)) #(영화제목과 주소4)개
    return "?"
    # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
    # return u'\n'.join(keywords)


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        keywords = answer(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

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
