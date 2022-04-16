########################################################################################################################
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# 텔레그램 bot 채팅방ID 확인
# https://api.telegram.org/bot5120813678:AAGz1vCMglGml4X5-eoTcFN3Y_JnWlFS6GY/getMe
# 1984552353
# 그룹채팅방 : -697051008
########################################################################################################################

########################################################################################################################
# 파일 생성이력
# 일자 / 작업자 / 내용
# 2022.04.11 / 이승호 / 텔레그램봇 명령어 입출력 처리및 로그, MariaDB SELECT 호출처리
# 2022.04.16 / 이승호 / 텔레그램봇 GitHub에 Push이벤트 발생시 DEV_PYTHON_GITHUB_BOT에서 메세지 출력처리(동작안됨)
########################################################################################################################

#import telegram
#from telegram import *
from telegram.ext import *

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
#  DEV_SERVER_BOT
#chat_room_id = 1984552353
#  DEV_PYTHON GROUP
chat_room_id = -697051008
my_server_env_os = platform.system()
my_server_env_os_det = platform.platform()
my_server_env_os_ver = platform.version()
my_server_env_cpu = platform.processor()
my_server_env_cpu_cnt = multiprocessing.cpu_count()
my_server_env_domain = "EXT IP ADDR : "+requests.get("https://api.ipify.org").text \
                                  + " / domain : dirtchamber.iptime.org "

# telegram bot setting
#my_bot = telegram.Bot(my_api_key)
#my_bot = Bot(my_api_key)
updater = Updater(token=my_api_key, use_context=True)  # bot에게 들어온 메시지가 있는지 체크
try:
    updater.dispatcher.stop()
    updater.job_queue.stop()
    updater.stop()
except Exception:
    err = traceback.format_exc()
    Errlog.SaveLog('ERR : '+str(err))
########################################################################################################################

########################################################################################################################
# 응답부 구현
# 명령어와 연결할 기능 구현
# 아래부터는 특정 커맨드를 입력받으면 출력을 처리하는 단일커맨드 예제를 처리
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
def Helprint(update, context):
    context.bot.sendMessage(chat_id=chat_room_id, text=" *** 사용가능한 명령어 리스트 입니다 *** "+"\n\n"
                                                      +" '/help' : 도움말 기능입니다. " + "\n\n"
                                                      +" '/set' : hi,토큰,서버에 대한 정보를 제공합니다. " + "\n\n"
                                                      +" '/google' : 구글에서 검색한 결과 url정보를 제공합니다." + "\n\n"
                                                      +" '/naver' : 네이버에서 검색한 결과 url정보를 제공합니다. " + "\n\n"
                                                      +" 그외 여러 기능들이 추가로 개발될 예정입니다. " + "\n\n")

# 아래부터는 특정 키워드를 입력받으면 출력을 처리하는 단일커맨드 예제를 처리
# (if 문을 이용한 처리 예제)
def BotSetPrinf(update, context):
    # 2022-04-09 : 사용자가 입력한 글자를 처리한다.
    keywords = ''
    for arg in context.args:
        keywords += '{}'.format(arg)

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

### 아래부터는 Web crawling을 통한 웹페이티 리스트 목록을 띄우는 예제를 처리

def BotGooglePrinf(update, context):
    # 입력한 검색어를 키워드변수에 조합한다.
    keywords = ''
    for arg in context.args:
        keywords += '{}'.format(arg)

    context.bot.sendMessage(chat_id=chat_room_id, text=keywords+" 구글 검색 결과입니다.")
    context.bot.sendMessage(chat_id=chat_room_id, text="https://www.google.com/search?q="+keywords)

def BotNaverPrinf(update, context):
    # 입력한 검색어를 키워드변수에 조합한다.
    keywords = ''
    for arg in context.args:
        keywords += '{}'.format(arg)

    context.bot.sendMessage(chat_id=chat_room_id, text=keywords+" 네이버 검색 결과입니다.")
    context.bot.sendMessage(chat_id=chat_room_id, text="https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="+keywords)

### 아래부터는 구글번역기를 돌려서 나온 결과값을 리턴처리


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
    # 아래 내용을 좀 어떻게 간소화 하고 싶은데 방법을 모르겠음.
    # 도움말 제공기능
    updater.dispatcher.add_handler(CommandHandler("help", Helprint))
    updater.dispatcher.add_handler(CommandHandler("HELP", Helprint))
    # 셋팅정보 제공
    updater.dispatcher.add_handler(CommandHandler('SET', BotSetPrinf, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('set', BotSetPrinf, pass_args=True))
    # 웹사이트 검색 기능
    updater.dispatcher.add_handler(CommandHandler('GOOGLE', BotGooglePrinf, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('Google', BotGooglePrinf, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('google', BotGooglePrinf, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('NAVER', BotNaverPrinf, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('Naver', BotNaverPrinf, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('naver', BotNaverPrinf, pass_args=True))
    # 구글 번역기 기능

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

