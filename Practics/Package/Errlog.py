########################################################################################################################
# 파일 생성이력
# 일자 / 작업자 / 내용
# 2022.04.11 / 이승호 / log파일 생성및 console화면에 출력처리
########################################################################################################################

# 용도 : 텔레그램봇에서 발생한 에러내용을 콘솔화면에 출력 또는 파일저장을 하기위한 파일
import logging # log기록

########################################################################################################################
## 전역변수
# log 설정
Log=logging.getLogger('DEV_PYTHON_BOT_LOG')

# log Format
#LogLevel = logging.ERROR
LogFileName = './DEV_PYTHON_BOT_Log.log'
LogFormat = logging.Formatter('[%(process)d | %(thread)d | %(levelname)s | %(filename)s:%(lineno)s] %(asctime)s: %(message)s')

# Console = 콘솔화면에 출력
ConsoleHandler = logging.StreamHandler()
ConsoleHandler.setFormatter(LogFormat)

# File = 파일에 저장처리
FileHandler = logging.FileHandler(LogFileName)
FileHandler.setFormatter(LogFormat)

# log set
#Log.setLevel(LogLevel)
Log.addHandler(ConsoleHandler)
Log.addHandler(FileHandler)
########################################################################################################################

########################################################################################################################
# 호출부 구현
def SaveLog(err):
    Log.error('ERR : '+str(err))
########################################################################################################################
