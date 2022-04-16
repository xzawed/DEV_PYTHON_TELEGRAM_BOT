########################################################################################################################
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# 텔레그램 bot 채팅방ID 확인
# https://api.telegram.org/bot5120813678:AAGz1vCMglGml4X5-eoTcFN3Y_JnWlFS6GY/getMe
# 1984552353
# -697051008
########################################################################################################################

########################################################################################################################
# 파일 생성이력
# 일자 / 작업자 / 내용
# 2022.04.11 / 이승호 / 텔레그램봇 명령어 입출력 처리및 로그, MariaDB SELECT 호출처리
# 2022.04.16 / 이승호 / 번역기능 추가(추후 기능 심화예정)
########################################################################################################################

# import os
#- os 모듈을 불러오는것
# from os import *
#- os모듈로부터 모두(*)import
# 언뜻보면 같은 의미인 것 같습니다만
# 조금 다르답니다.어떻게 다른지 결론부터 말씀드리면 아래와 같습니다.
## 한줄요약 ##
#import만 사용하면 모듈 안의 함수를 사용할 때, 모듈명.함수명()으로 하고, from을 사용하면 바로 함수명()으로 사용

#import telegram
#from telegram import *
from telegram.ext import *
from googletrans import *

# SERVER 환경설정을 위한내용
import platform
#import socket # 내부IP 확인용
import multiprocessing
import requests
import traceback # traceback 프로그램 에러

# 개별적으로 생성한내용
import mysql
import Errlog
########################################################################################################################
## 전역변수
# telegram token key와 chat room id 입력
my_api_key = "5120813678:AAGz1vCMglGml4X5-eoTcFN3Y_JnWlFS6GY"
chat_room_id = -697051008
my_server_env_os = platform.system()
my_server_env_os_det = platform.platform()
my_server_env_os_ver = platform.version()
my_server_env_cpu = platform.processor()
my_server_env_cpu_cnt = multiprocessing.cpu_count()
my_server_env_domain = "EXT IP ADDR : "+requests.get("https://api.ipify.org").text \
                                  + " / domain : dirtchamber.iptime.org "

# telegram bot setting
updater = Updater(token=my_api_key, use_context=True)  # bot에게 들어온 메시지가 있는지 체크

try:
    updater.dispatcher.stop()
    updater.job_queue.stop()
    updater.stop()
except Exception:
    err = traceback.format_exc()
    Errlog.SaveLog(str(err))
########################################################################################################################

########################################################################################################################
# 응답부 구현
# 명령어와 연결할 기능 구현
# 아래부터는 특정 커맨드를 입력받으면 출력을 처리하는 단일커맨드 예제를 처리
def HelpPrint(update, context):
    try:
        context.bot.sendMessage(chat_id=chat_room_id, text=" *** 사용가능한 명령어 리스트 입니다 *** " + "\n\n" +
                                                           " '/help' : 도움말 기능입니다. " + "\n\n" +
                                                           " '/set' : hi,토큰,서버에 대한 정보를 제공합니다. " + "\n\n" +
                                                           " '/google' : 구글에서 검색한 결과 url정보를 제공합니다. " + "\n\n" +
                                                           " '/naver' : 네이버에서 검색한 결과 url정보를 제공합니다. " + "\n\n" +
                                                           " '/tran' : 구글번역을 통한 한글을 영문으로 변환하여 출력합니다(추후 기능추가). " + "\n\n" +
                                                           " 그외 여러 기능들이 추가로 개발될 예정입니다.")
    except Exception:
        err = traceback.format_exc()
        Errlog.SaveLog(str(err))

#def HelloPrint(update, context):
#    context.bot.sendMessage(chat_id=chat_room_id, text="hello~")
#
#def TokenPrint(update, context):
#    context.bot.sendMessage(chat_id=chat_room_id, text="텔레그램봇 Token값은 ( "+str(my_api_key)+" ) 입니다.")
#
#def ChatIDPrint(update, context):
#    context.bot.sendMessage(chat_id=chat_room_id, text="채팅방ID는 ( "+str(chat_room_id)+" ) 입니다.")
#
#def ServerENVPrint(update, context):
#    context.bot.sendMessage(chat_id=chat_room_id, text=" ***텔레그램 BOT 개발서버 정보*** "+"\n"
#                                                      +" OS : "+str(my_server_env_os)+"\n\n"
#                                                      +"         "+str(my_server_env_os_det)+"\n\n"
#                                                      +"         "+str(my_server_env_os_ver)+"\n\n"
#                                                      +"         "+str(my_server_env_domain)+"\n\n"
#                                                      +" CPU : "+str(my_server_env_cpu)+"\n\n"
#                                                      +" CPU 갯수 : "+str(my_server_env_cpu_cnt) )

# 아래부터는 특정 키워드를 입력받으면 출력을 처리하는 단일커맨드 예제를 처리
# (if 문을 이용한 처리 예제)
def BotSetPrinf(update, context):
    try:
        # 2022-04-09 : 사용자가 입력한 글자를 처리한다.
        keywords = ''
        for arg in context.args:
            keywords += '{}'.format(arg)+" "

    #    context.bot.sendMessage(chat_id=chat_room_id, text=keywords)
        # 하단내용은 상단의 내용이 문제가 해결된 이후에 수정해야할듯..
        # 2022-04-09 : 상단에서 입력받은 값을 토대로 해당되는 결과값을 Return 한다.
        if   keywords == "hi":
            context.bot.sendMessage(chat_id=chat_room_id, text="hello~")
        elif keywords == "토큰":
            context.bot.sendMessage(chat_id=chat_room_id, text="텔레그램봇 Token값은 ( "+str(my_api_key)+" ) 입니다.")
        elif keywords == "서버":
            context.bot.sendMessage(chat_id=chat_room_id, text=" ***텔레그램 BOT 개발서버 정보*** " + "\n"
                                                             + " OS : " + str(my_server_env_os) + "\n\n"
                                                             + "         " + str(my_server_env_os_det) + "\n\n"
                                                             + "         " + str(my_server_env_os_ver) + "\n\n"
                                                             + "         " + str(my_server_env_domain) + "\n\n"
                                                             + " CPU : " + str(my_server_env_cpu) + "\n\n"
                                                             + " CPU 갯수 : " + str(my_server_env_cpu_cnt))
        else :
            context.bot.sendMessage(chat_id=chat_room_id, text=keywords+" 은(는) 아직 설정되지 않은 단어입니다")
    except Exception:
        err = traceback.format_exc()
        Errlog.SaveLog(str(err))

### 아래부터는 웹사이트 검색기능 처리
def BotGooglePrinf(update, context):
    try:
        # 입력한 검색어를 키워드변수에 조합한다.
        keywords = ''
        for arg in context.args:
            keywords += '{}'.format(arg)+"+"

        # 맨마지막 글자 1자리를 제거한다(+)문자 제거
        keywords = keywords[:-1]

        context.bot.sendMessage(chat_id=chat_room_id, text=keywords+" 구글 검색")
        context.bot.sendMessage(chat_id=chat_room_id, text="https://www.google.com/search?q="+keywords)
    except Exception:
        err = traceback.format_exc()
        Errlog.SaveLog(str(err))

def BotNaverPrinf(update, context):
    try:
        # 입력한 검색어를 키워드변수에 조합한다.
        keywords = ''
        for arg in context.args:
            keywords += '{}'.format(arg)+"+"

        # 맨마지막 글자 1자리를 제거한다(+)문자 제거
        keywords = keywords[:-1]

        context.bot.sendMessage(chat_id=chat_room_id, text=keywords+" 네이버 검색")
        context.bot.sendMessage(chat_id=chat_room_id, text="https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="+keywords)
    except Exception:
        err = traceback.format_exc()
        Errlog.SaveLog(str(err))

### 아래부터는 입력받은 메세지를 번역하는 기능을 제공
def BotGoogleTranPrinf(update, context):
    try:
        keywords = ''
        # 사용자가 입력한 단어를 문장으로 가공한다.
        for arg in context.args:
            keywords += '{}'.format(arg)+" "

        translator = Translator()

        # 번역대상 언어와 번역처리 언어를 추후 사용자가 지정할수 있게 처리 예정.
        content = translator.translate(keywords,src='ko',dest='en')

        # 번역한 문장을 변수처리
        sentence = content.text

        context.bot.sendMessage(chat_id=chat_room_id, text=keywords+" 구글번역")
        context.bot.sendMessage(chat_id=chat_room_id, text=sentence)
    except Exception:
        err = traceback.format_exc()
        Errlog.SaveLog(str(err))

### 아래부터는 주기적으로 특정메세지를 띄우는 예제를 처리


########################################################################################################################

########################################################################################################################
# 호출부 구현
# 기능과 명령어 연결("/hi" 명령어가 들어오면 TestPrint 함수가 실행됨)
# 참고로 한글명령어가 안됨..
#updater.dispatcher.add_handler(CommandHandler("hi", HelloPrint))
#updater.dispatcher.add_handler(CommandHandler("token", TokenPrint))
#updater.dispatcher.add_handler(CommandHandler("chatid", ChatIDPrint))
#updater.dispatcher.add_handler(CommandHandler("server", ServerENVPrint))

# 하단에 pass_args를 통해서 키워드 입력받은 내용을 처리하는듯한데..잘안됨.
# 대소문자별로 셋팅
try:
    mysql.SelMysql(opt='START')
    # 아래 내용을 어떻게 정리를 하면 좋을까..
    # command값을 upper로 일괄 변환해서 실행처리 가능할지 모르겠음.
    updater.dispatcher.add_handler(CommandHandler("help".upper(), HelpPrint))
    updater.dispatcher.add_handler(CommandHandler('set'.upper(), BotSetPrinf, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('google'.upper(), BotGooglePrinf, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('naver'.upper(), BotNaverPrinf, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('tran'.upper(), BotGoogleTranPrinf, pass_args=True))

    mysql.SelMysql(opt='END')
    err = traceback.format_exc()
    Errlog.SaveLog(str(err))
except Exception:
    err = traceback.format_exc()
    Errlog.SaveLog(str(err))
########################################################################################################################

########################################################################################################################
# 시작
updater.start_polling()
updater.idle()
########################################################################################################################

