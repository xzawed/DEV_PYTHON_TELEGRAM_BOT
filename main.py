########################################################################################################################
#  This is a sample Python script.
#  Press Shift+F10 to execute it or replace it with your code.
#  Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#  텔레 그램 bot 채팅방 ID 확인
#  https://api.telegram.org/bot5120813678:AAGz1vCMglGml4X5-eoTcFN3Y_JnWlFS6GY/getMe
#  개인 : 1984552353
#  그룹 : -697051008
########################################################################################################################

########################################################################################################################
#  파일 생성 이력
#  일자 / 작업자 / 내용
#  2022.04.11 / 이승호 / 텔레 그램 봇 명령어 입출력 처리및 로그, MariaDB SELECT 호출 처리
#  2022.04.16 / 이승호 / 번역 기능 추가(추후 기능 심화 예정)
########################################################################################################################

#  import os
#  - os 모듈을 불러 오는 것
#  from os import *
#  - os 모듈 로부터 모두(*)import
#  언뜻 보면 같은 의미인 것 같 습니다 만
#  조금 다르 답니다.어떻게 다른지 결론 부터 말씀 드리면 아래와 같 습니다.
#  --  한줄 요약  --
#  import 만 사용 하면 모듈 안의 함수를 사용할 때, 모듈명.함수명()으로 하고, from 을 사용 하면 바로 함수명()으로 사용

#  import telegram
#  from telegram import *
from telegram.ext import *
from googletrans import *

#  SERVER 환경 설정을 위한 내용
import platform
#  내부 IP 확인용
#  import socket
import multiprocessing
import requests

#  SSH 접속
#  cryptography ver: 36.0.2 down
import paramiko

import datetime

#  개별적 으로 생성한 내용
import mysql
import Errlog
########################################################################################################################

#  전역 변수
#  telegram token key 와 chat room id 입력
my_api_key = mysql.selmysql('TOKEN', ('TELEGRAM', '@xzawed_bot'))
chat_room_id = -697051008
my_server_env_os = platform.system()
my_server_env_os_det = platform.platform()
my_server_env_os_ver = platform.version()
my_server_env_cpu = platform.processor()
my_server_env_cpu_cnt = multiprocessing.cpu_count()
my_server_env_domain = "EXT IP ADDR : "+requests.get("https://api.ipify.org").text \
                                  + " / domain : xzawed.iptime.org "
#  telegram bot setting
updater = Updater(token=my_api_key, use_context=True)  # bot 에게 들어온 메시지 가 있는지 체크

try:
    updater.dispatcher.stop()
    updater.job_queue.stop()
    updater.stop()
except Exception:
    Errlog.savelog('ERROR')

########################################################################################################################

def execcommands():
    #  SSH Client 접속 - 추후 해당 내용은 DB 에서 불러 오는 내용 으로 수정 예정
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    #  pwd = getpass.getpass("devuser11!")
    cli.connect("xzawed.iptime.org", port=2153, username="devuser", password="devuser11!", look_for_keys=False, allow_agent=False)

    #  명령어 실행
    #  실행 결과를 표준 콘솔 입력(stdin), 표준 콘솔 출력(stdout), 표준 에러 출력(stderr)에 리턴 한다.
    stdin, stdout, stderr = cli.exec_command("jupyter-notebook list")
    #   실행한 명령어 에 대한 결과 텍스트
    lines = stdout.readlines()
    resultdata = ''.join(lines)

    resultdata = resultdata[resultdata.find('?')+1:resultdata.find('::')]

    print(resultdata)  # 결과 확인

    cli.close()

    return resultdata

########################################################################################################################
#  응답부 구현
#  명령어 와 연결할 기능 구현
#  아래 부터는 특정 커맨드 를 입력 받으면 출력을 처리 하는 단일 커맨드 예제를 처리
def helpprinf(update, context):
    try:
        context.bot.sendMessage(chat_id=chat_room_id, text=" *** 사용 가능한 명령어 리스트 입니다 *** " + "\n\n" +
                                                           " '/help' : 도움말 기능 입니다. " + "\n\n" +
                                                           " '/set' : hi,토큰,서버에 대한 정보를 제공 합니다. " + "\n\n" +
                                                           " '/google' : 구글 에서 검색한 결과 url 정보 를 제공 합니다. " + "\n\n" +
                                                           " '/naver' : 네이버 에서 검색한 결과 url 정보 를 제공 합니다. " + "\n\n" +
                                                           " '/tran' : 구글 번역 을 통한 한글을 영문 으로 변환 하여 출력 합니다. " + "\n\n" +
                                                           " 그외 여러 기능 들이 추가로 개발될 예정 입니다.")
    except Exception:
        Errlog.savelog('ERROR')

#  아래 부터는 특정 키워드 를 입력 받으면 출력을 처리 하는 단일 커맨드 예제를 처리
#  (if 문을 이용한 처리 예제)
def botsetprinf(update, context):
    try:
        #  2022-04-09 : 사용자 가 입력한 글자를 처리 한다.
        keywords = ''
        for arg in context.args:
            keywords += '{}'.format(arg)+" "

        #  맨 마지막 글자 1자리를 제거 한다(+)문자 제거
        keywords = keywords[:-1]

        #  context.bot.sendMessage(chat_id=chat_room_id, text=keywords)
        #  2022-04-09 : 상단 에서 입력 받은 값을 토대로 해당 되는 결과 값을 Return 한다.
        if   keywords == "hi":
            context.bot.sendMessage(chat_id=chat_room_id, text="hello~")
        elif keywords == "서버":
            context.bot.sendMessage(chat_id=chat_room_id, text=" ***텔레 그램 BOT 개발 서버 정보*** " + "\n"
                                                             + " OS : " + str(my_server_env_os) + "\n\n"
                                                             + "         " + str(my_server_env_os_det) + "\n\n"
                                                             + "         " + str(my_server_env_os_ver) + "\n\n"
                                                             + "         " + str(my_server_env_domain) + "\n\n"
                                                             + " CPU : " + str(my_server_env_cpu) + "\n\n"
                                                             + " CPU 갯수 : " + str(my_server_env_cpu_cnt))
        elif keywords == "토큰":
            jupyter_token = execcommands()
            context.bot.sendMessage(chat_id=chat_room_id, text=" jupyter token : "+jupyter_token)
        else :
            context.bot.sendMessage(chat_id=chat_room_id, text=keywords+" 은(는) 아직 설정 되지 않은 단어 입니다")
    except Exception:
        Errlog.savelog('ERROR')

#  아래 부터는 웹 사이트 검색 기능 처리
def botgoogleprinf(update, context):
    try:
        #  입력한 검색어 를 키워드 변수에 조합 한다.
        keywords = ''
        for arg in context.args:
            keywords += '{}'.format(arg)+"+"

        #  맨 마지막 글자 1자리를 제거 한다(+)문자 제거
        keywords = keywords[:-1]
        url = "https://www.google.com/search?q="
        context.bot.sendMessage(chat_id=chat_room_id, text=keywords+" 구글 검색")
        context.bot.sendMessage(chat_id=chat_room_id, text=url+keywords)
    except Exception:
        Errlog.savelog('ERROR')

def botnaverprinf(update, context):
    try:
        #  입력한 검색어 를 키워드 변수에 조합 한다.
        keywords = ''
        for arg in context.args:
            keywords += '{}'.format(arg)+"+"

        #  맨 마지막 글자 1자리를 제거 한다(+)문자 제거
        keywords = keywords[:-1]
        url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="
        context.bot.sendMessage(chat_id=chat_room_id, text=keywords+" 네이버 검색")
        context.bot.sendMessage(chat_id=chat_room_id, text=url+keywords)
    except Exception:
        Errlog.savelog('ERROR')

#  아래 부터는 입력 받은 메세지 를 번역 하는 기능을 제공
def botgoogletranprinf(update, context):
    try:
        keywords = ''
        #  사용자 가 입력한 단어를 문장 으로 가공 한다.
        for arg in context.args:
            keywords += '{}'.format(arg)+" "

        translator = Translator()

        #  번역 대상 언어와 번역 처리 언어를 추후 사용자 가 지정 할수 있게 처리 예정.
        content = translator.translate(keywords, src='ko', dest='en')

        #  번역한 문장을 변수 처리
        sentence = content.text

        context.bot.sendMessage(chat_id=chat_room_id, text=keywords+" 구글 번역")
        context.bot.sendMessage(chat_id=chat_room_id, text=sentence)
    except Exception:
        Errlog.savelog('ERROR')

def botdateprinf(update, context):
    try:
        #  입력한 검색어 를 키워드 변수에 조합 한다.
        keywords = ''
        for arg in context.args:
            keywords += '{}'.format(arg)+"+"

        #  맨 마지막 글자 1자리를 제거 한다(+)문자 제거
        keywords = keywords[:-1]

        #  날짜 포멧과 요일 포멧
        format_date = '%Y-%m-%d'
        format_week = '%w'
        str_date = str(keywords)

        #  입력 받은 값의 길이가 8자리 일 경우
        if len(str_date) == 8:
            str_date = str_date[0:4]+"-"+str_date[4:6]+"-"+str_date[6:8]

        #  1주
        one_week = datetime.timedelta(weeks=1)

        #  날짜형
        #  현재 일자
        try:
            dt_date = datetime.datetime.strptime(str_date, format_date)
        except Exception:
            dt_date = datetime.datetime.now()

        #  문자형
        dy_str_date = dt_date.strftime(format_week)
        #  숫자형
        dy_int_date = int(dy_str_date)
        dy_calc_date = dy_int_date
        #  현재 일자 기준 현재 주차의 월요일 을 구한다.

        i = 0
        while dy_calc_date >= 1:
            dy_calc_date = dy_int_date-i
            if dy_calc_date == 1:
                break
            else:
                i += 1

        if dy_int_date == 0:
            i = 6

        #  입력한 날짜의 해당 주차의 월요일
        mon_date = dt_date - datetime.timedelta(days=i)
        #  다음주 일요일
        nw_date = mon_date + one_week - datetime.timedelta(days=1)

        #  문자형 으로 변경
        dt_str_date = datetime.datetime.strftime(dt_date, format_date)
        mon_str_date = datetime.datetime.strftime(mon_date, format_date)
        nw_str_date = datetime.datetime.strftime(nw_date, format_date)

        #  print(dt_date)
        #  print(mon_date)
        #  print(nw_date)
        #  print(dy_str_date)
        #  print(i)

        context.bot.sendMessage(chat_id=chat_room_id, text="현재 일자 : "+dt_str_date + "\n"
                                                           "금주 월요일 : "+mon_str_date + "\n"
                                                           "금주 일요일 : "+nw_str_date)
    except Exception:
        Errlog.savelog('ERROR')

#  아래 부터는 주기적 으로 특정 메세지 를 띄우는 예제를 처리


########################################################################################################################

########################################################################################################################
#  호출부 구현
#  기능과 명령어 연결("/hi" 명령어 가 들어 오면 TestPrint 함수가 실행됨)
#  참고로 한글 명령어 가 안됨.
try:
    #  command 값을 upper 로 일괄 변환 해서 실행 처리
    Errlog.savelog('INFO')
    updater.dispatcher.add_handler(CommandHandler("help".upper(), helpprinf))
    updater.dispatcher.add_handler(CommandHandler('set'.upper(), botsetprinf, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('google'.upper(), botgoogleprinf, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('naver'.upper(), botnaverprinf, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('tran'.upper(), botgoogletranprinf, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('date'.upper(), botdateprinf, pass_args=True))
    mysql.selmysql('TEMP', '실행')

    #  err = traceback.format_exc()
    #  Errlog.saveLog('INFO', str(err))
except Exception:
    Errlog.savelog('ERROR')
########################################################################################################################

########################################################################################################################
#  시작
updater.start_polling()
updater.idle()
########################################################################################################################
