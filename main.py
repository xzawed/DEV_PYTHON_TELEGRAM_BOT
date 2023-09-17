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
#  Slack에 연동 확인 테스트
#  2023.09.10 python-telegram-bot 이 버전업으로 인해 변경됨에 따라 하단의 기존코드 내용을 수정작업
#             dispatcher를 통해 이벤트 핸들러를 처리하는 방식에서 application을 통해 비동기 방식으로 변경
#             기존의 dispatcher.add_handler(CommandHandler("명령어", 함수명)) 방식에서
#             application.add_handler(CommandHandler("명령어", 함수명)) 방식으로 변경
#             참고 : https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.html
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
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, ContextTypes

#  Google 번역기능
#  from googletrans import *

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
from mysql import *
import Errlog
import DateUtil
import psutil
########################################################################################################################

#  전역 변수
#  telegram token key 와 chat room id 입력
DB = MYSQL()

my_api_key = DB.selmysql(opt='TOKEN', data=('TELEGRAM', '@xzawed_bot'))
#  chat_room_id = -697051008

my_server_env_os = platform.system()
my_server_env_os_det = platform.platform()
my_server_env_os_ver = platform.version()
my_server_env_cpu = platform.processor()
my_server_env_cpu_cnt = multiprocessing.cpu_count()
my_server_cpu_frq = psutil.cpu_freq()
my_server_env_cpu_frq = round( my_server_cpu_frq.current / 1000, 2)
my_server_memory = psutil.virtual_memory()
my_server_env_memory = round(my_server_memory.total / 1024**3)
# my_server_env_domain = "EXT IP ADDR : "+format(requests.get("https://api.ipify.org").text)+ " / domain : xzawed.iptime.org "
my_server_env_domain = " domain : xzawed.iptime.org "

myapp = Application.builder().token(my_api_key).build()


########################################################################################################################
def execcommands():
    #  SSH Client 접속 - 추후 해당 내용은 DB 에서 불러 오는 내용 으로 수정 예정
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    #  pwd = getpass.getpass("devuser11!")
    cli.connect(hostname="xzawed.iptime.org", port=22, username="devuser", password="devuser", look_for_keys=False, allow_agent=False)
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
async def helpprinf(update: Update, context: CallbackContext):
    try:
        await update.message.reply_text(" *** 사용 가능한 명령어 리스트 입니다 *** " + "\n\n" +
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
async def botsetprinf(update: Update, context: CallbackContext):
    try:
        user = update.effective_user

        #  context.bot.sendMessage(chat_id=chat_room_id, text=keywords)
        #  2022-04-09 : 상단 에서 입력 받은 값을 토대로 해당 되는 결과 값을 Return 한다.
        if   update.message.text.find("hi") >= 0:
            await update.message.reply_text("hello~")
        elif update.message.text.find("서버") >= 0:
            await update.message.reply_text(" ***텔레 그램 BOT 개발 서버 정보*** " + "\n"
                                          + " OS : " + str(my_server_env_os) + "\n\n"
                                          + "         " + str(my_server_env_os_det) + "\n\n"
                                          + "         " + str(my_server_env_os_ver) + "\n\n"
                                          + "         " + str(my_server_env_domain) + "\n\n"
                                          + " CPU : " + str(my_server_env_cpu) + "\n\n"
                                          + "       " + str(my_server_env_cpu_frq) +"GHz"+ "\n\n"
                                          + " CPU 갯수 : " + str(my_server_env_cpu_cnt) +"Core"+ "\n\n"
                                          + " MEMORY : " + str(my_server_env_memory)+ "GB")

        elif update.message.text.find("토큰") >= 0:
            jupyter_token = execcommands()
            await update.message.reply_text(" jupyter token : "+jupyter_token)
        else :
            await update.message.reply_text(" 은(는) 아직 설정 되지 않은 단어 입니다")
    except Exception:
        Errlog.savelog('ERROR')


#  아래 부터는 웹 사이트 검색 기능 처리
async def botgoogleprinf(update: Update, context: CallbackContext):
    try:
        user = update.effective_user
        keywords = update.message.text.lower()

        url = "https://www.google.com/search?q="
        await update.message.reply_text(keywords+" 구글 검색")
        await update.message.reply_text(url+keywords)
    except Exception:
        Errlog.savelog('ERROR')


async def botnaverprinf(update: Update, context: CallbackContext):
    try:
        user = update.effective_user
        #  입력한 검색어 를 키워드 변수에 조합 한다.
        keywords = update.message.text.lower()

        url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="
        await update.message.reply_text(keywords+" 네이버 검색")
        await update.message.reply_text(url+keywords)
    except Exception:
        Errlog.savelog('ERROR')


#  아래 부터는 입력 받은 메세지 를 번역 하는 기능을 제공
async def botgoogletranprinf(update: Update, context: CallbackContext):
    try:
        user = update.effective_user
        keywords = update.message.text.lower()

        translator = Translator()

        #  번역 대상 언어와 번역 처리 언어를 추후 사용자 가 지정 할수 있게 처리 예정.
        content = translator.translate(keywords, src='ko', dest='en')

        #  번역한 문장을 변수 처리
        sentence = content.text

        await update.message.reply_text(keywords+" 구글 번역")
        await update.message.reply_text(sentence)
    except Exception:
        Errlog.savelog('ERROR')


#  입력받은 날짜 해당주차의 첫날짜와 마지막 날짜를 구함
async def botdateprinf(update: Update, context: CallbackContext):
    try:
        user = update.effective_user
        keywords = update.message.text.lower()

        #  날짜 포멧과 요일 포멧
        format_date = '%Y-%m-%d'
        str_date = str(keywords)

        #  입력 받은 값의 길이가 8자리 일 경우
        if len(str_date) == 8:
            str_date = str_date[0:4]+"-"+str_date[4:6]+"-"+str_date[6:8]

        #  날짜형
        #  현재 일자
        try:
            dt_date = datetime.datetime.strptime(str_date, format_date)
        except Exception:
            dt_date = datetime.datetime.now()

        today = DateUtil.DateUtil(dt_date)

        dt_now_date = datetime.datetime.strftime(dt_date,format_date)
        dt_week_fst_date = datetime.datetime.strftime(today.getWeekFirstDate(),format_date)
        dt_week_lst_date = datetime.datetime.strftime(today.getWeekLastDate(), format_date)

        await update.message.reply_text("현재 일자 : "+dt_now_date + "\n"
                                        "금주 월요일 : "+dt_week_fst_date + "\n"
                                        "금주 일요일 : "+dt_week_lst_date)
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
    myapp.add_handler(CommandHandler("help".upper(), helpprinf))
    myapp.add_handler(CommandHandler('set'.upper(), botsetprinf, has_args=True))
    myapp.add_handler(CommandHandler('google'.upper(), botgoogleprinf, has_args=True))
    myapp.add_handler(CommandHandler('naver'.upper(), botnaverprinf, has_args=True))
    myapp.add_handler(CommandHandler('tran'.upper(), botgoogletranprinf, has_args=True))
    myapp.add_handler(CommandHandler('date'.upper(), botdateprinf, has_args=True))
    DB.selmysql(opt='TEMP', data='실행')

    #  err = traceback.format_exc()
    #  Errlog.saveLog('INFO', str(err))
except Exception:
    Errlog.savelog('ERROR')
########################################################################################################################

########################################################################################################################
#  시작
myapp.run_polling()
########################################################################################################################
