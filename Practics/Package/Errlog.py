########################################################################################################################
#  파일 생성 이력
#  일자 / 작업자 / 내용
#  2022.04.11 / 이승호 / log 파일 생성및 console 화면에 출력 처리
########################################################################################################################

#  용도 : 텔레 그램 봇 에서 발생한 에러 내용을 콘솔 화면에 출력 또는 파일 저장을 하기 위한 파일
#  log 기록
import logging
#  traceback 프로 그램 에러
import traceback

import mysql

########################################################################################################################
#  전역 변수
#  log 설정
Log = logging.getLogger('DEV_PYTHON_TELEGRAM_BOT_LOG')

#  log Format
#  LogLevel = logging.ERROR
LogFileName = './Practics/log/DEV_PYTHON_TELEGRAM_BOT_Log.log'
#  LogFormat = logging.Formatter('[%(process)d | %(thread)d | %(levelname)s | %(filename)s:%(lineno)s]
#                                 %(asctime)s: %(message)s')
LogFormat = logging.Formatter('TELEGRAM|[%(process)d | %(thread)d | %(filename)s:%(lineno)s] '
                              '|::|%(levelname)s|::| %(asctime)s: %(message)s')

#  Console = 콘솔 화면에 출력
ConsoleHandler = logging.StreamHandler()
ConsoleHandler.setFormatter(LogFormat)

#  File = 파일에 저장 처리
FileHandler = logging.FileHandler(LogFileName)
FileHandler.setFormatter(LogFormat)

#  log set
#  Log.setLevel(LogLevel)
Log.addHandler(ConsoleHandler)
Log.addHandler(FileHandler)
########################################################################################################################


########################################################################################################################
#  호출부 구현
def savelog(state):
    log = traceback.format_exc()

    if state == "INFO":
        Log.info('MESSAGE : '+str(log))
    elif state == "ERROR":
        Log.error('MESSAGE : '+str(log))

    DB = mysql.MYSQL
    DB.selmysql(self=DB ,opt='LOG', data=(state, str(log)))
    print(state+" : "+str(log))
########################################################################################################################
