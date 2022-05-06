########################################################################################################################
#  파일 생성이력
#  일자 / 작업자 / 내용
#  2022.04.11 / 이승호 / log파일 생성및 console화면에 출력처리
########################################################################################################################

#  용도 : 텔레그램봇에서 발생한 에러내용을 콘솔화면에 출력 또는 파일저장을 하기위한 파일
#  log기록
import logging
#  traceback 프로그램 에러
import traceback

import mysql

########################################################################################################################
#  전역변수
#  log 설정
Log = logging.getLogger('DEV_PYTHON_TELEGRAM_BOT_LOG')

#  log Format
#  LogLevel = logging.ERROR
LogFileName = './Practics/log/DEV_PYTHON_TELEGRAM_BOT_Log.log'
#  LogFormat = logging.Formatter('[%(process)d | %(thread)d | %(levelname)s | %(filename)s:%(lineno)s] %(asctime)s: %(message)s')
LogFormat = logging.Formatter('TELEGRAM|[%(process)d | %(thread)d | %(filename)s:%(lineno)s] |::|%(levelname)s|::| %(asctime)s: %(message)s')

#  Console = 콘솔화면에 출력
ConsoleHandler = logging.StreamHandler()
ConsoleHandler.setFormatter(LogFormat)

#  File = 파일에 저장처리
FileHandler = logging.FileHandler(LogFileName)
FileHandler.setFormatter(LogFormat)

#  log set
#  Log.setLevel(LogLevel)
Log.addHandler(ConsoleHandler)
Log.addHandler(FileHandler)
########################################################################################################################

########################################################################################################################
#  호출부 구현
def saveLog(state):
    log = traceback.format_exc()

    if   state == "INFO":
        Log.info('MESSAGE : '+str(log))
    elif state == "ERROR":
        Log.error('MESSAGE : '+str(log))

    mysql.selmysql('LOG', (state, str(log)))
    print(state+" : "+str(log))
########################################################################################################################
