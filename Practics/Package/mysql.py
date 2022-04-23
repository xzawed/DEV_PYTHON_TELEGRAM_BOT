########################################################################################################################
#  파일 생성이력
#  일자 / 작업자 / 내용
#  2022.04.11 / 이승호 / MariaDB내에 텔레그램 메세지및 로그기록 정보를 저장하기 위함
########################################################################################################################

#  텔레그램봇에서 발생한 송수신한 정보를 DB기록하기 위한 처리부
#  MariaDB
import pymysql
#  traceback 프로그램 에러
import traceback

#  개별적으로 생성한내용
import Errlog

#  connection 정보
#  host= 연결주소 ip or 도메인
#  port = 포트번호
#  user = ID
#  password = 암호
#  db = 데이터베이스명
#  charset = 'utf8',
#  autocommit = 자동으로 commit 처리할지 여부
#  cursorclass = 커서타입 ( https://pymysql.readthedocs.io/en/latest/modules/cursors.html ) 참조
########################################################################################################################
#  전역변수
"""
db = pymysql.connect(
    host='dirtchamber.iptime.org',  # host name (연결주소)
    port=13306,
    user='root',  # user name (ID)
    password='root',  # password (암호)
    db='DEV_MARIADB',  # db name (데이터베이스명)
    charset='utf8',
    autocommit=False,
    cursorclass=pymysql.cursors.DictCursor
)
#  DB와 관련된 커서 객체를 생성한다
curs = db.cursor()
"""
########################################################################################################################

########################################################################################################################
#  호출부 구현
#  class개념
class MariaDB:
    #  MariaDB setting
    def sessionmysql(self):
        self.db = pymysql.connect(
                                    host='xzawed.iptime.org',
                                    port=13306,
                                    user='root',
                                    password='root',
                                    db='DEV_MARIADB',
                                    charset='utf8',
                                    autocommit=False,
                                    cursorclass=pymysql.cursors.DictCursor
                                 )
        #  DB와 관련된 커서 객체를 생성한다
        self.curs = self.db.cursor()

    #  MariaDB 연결이후 SELECT, UPDATE, INSERT, DELETE 에 해당되는 내용을 호출처리
    def startmysql(self):
        sql = "SELECT 'A';"
        self.curs.execute(sql)
        print("정상적으로 시작 되었습니다.")

    def endmysql(self):
        sql = "SELECT 'A';"
        self.curs.execute(sql)
        print("정상적으로 종료 되었습니다.")

    def tokenmysql(self):
        sql = "SELECT TOKEN FROM BOT_TOKEN WHERE COMCD = %s AND BOT_ID = %s; "
        self.curs.execute(sql, ('TELEGRAM', '@xzawed_bot'))
        token_list = self.curs.fetchall()

        for x in token_list:
            #  print(x['TOKEN'])
            xzawed_token = x['TOKEN']

        return xzawed_token

    def logmysql(self,data):
        sql = "INSERT INTO TELEGRAM_BOT_LOG ( SEQ, WRITE_DATE, STATE, LOG ) VALUES ( nextval(JOB_LOG_SEQ) SYSDATE(), %s, %s ) "
        self.curs.execute(sql, data)
        self.db.commit()

    #  MariaDB Close
    def closemysql(self):
        self.curs.close()
########################################################################################################################

########################################################################################################################
#  전역함수처리(외부에서 호출할때 쓰임)
def selmysql(opt, data):
    try:
        result = ""
        MariaDB.sessionmysql(MariaDB)

        if   opt == "START":
            MariaDB.startmysql(MariaDB)
        elif opt == "END":
            MariaDB.endmysql(MariaDB)
        elif opt == "TOKEN":
            result = MariaDB.tokenmysql(MariaDB)
        elif opt == "LOG":
            MariaDB.logmysql(MariaDB, data)

        MariaDB.closemysql(MariaDB)

        return result
    except Exception:
        err = traceback.format_exc()
        Errlog.SaveLog(str(err))
########################################################################################################################
