########################################################################################################################
#  파일 생성 이력
#  일자 / 작업자 / 내용
#  2022.04.11 / 이승호 / Maria DB 내에 텔레 그램 메세지 및 로그 기록 정보를 저장 하기 위함
########################################################################################################################

#  텔레 그램 봇 에서 발생한 송 수신한 정보를 DB 기록 하기 위한 처리부
#  MariaDB
import pymysql

#  개별적 으로 생성한 내용
import Errlog


#  connection 정보
#  host= 연결 주소 ip or 도메인
#  port = 포트 번호
#  user = ID
#  password = 암호
#  db = 데이터 베이스 명
#  charset = 'utf8',
#  autocommit = 자동 으로 commit 처리 할 지 여부
#  cursorclass = 커서 타입 ( https://pymysql.readthedocs.io/en/latest/modules/cursors.html ) 참조
########################################################################################################################

########################################################################################################################
#  호출부 구현
#  class 개념


class MariaDB:

    #  MariaDB setting
    sql = ""
    db = type(None)
    curs = type(None)
    def conn(self):
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
    def getcurs(self) :
        self.curs = self.db.cursor()

    def closemysql(self) :
        self.db.close()

    #  MariaDB 연결 이후 SELECT, UPDATE, INSERT, DELETE 에 해당 되는 내용을 호출 처리
    def tempmysql(self, data):
        self.sql = "SELECT %s RESULT;"
        self.curs.execute(self.sql, data)
        result = self.curs.fetchall()
        message = ""
        for x in result:
            #  print(x['TOKEN'])
            message = x['RESULT']

        print("정상 적으로 " + message + " 되었 습니다.")

    def tokenmysql(self, data):
        self.sql = "SELECT TOKEN FROM BOT_TOKEN WHERE COMCD = %s AND BOT_ID = %s; "
        self.curs.execute(self.sql, data)
        token_list = self.curs.fetchall()
        xzawed_token = ""
        for x in token_list:
            #  print(x['TOKEN'])
            xzawed_token = x['TOKEN']

        return xzawed_token

    def logmysql(self, data):
        self.sql = "INSERT INTO BOT_LOG ( SEQ, WRITE_DATE, STATE, LOG, COMCD ) VALUES ( nextval(JOB_LOG_SEQ), SYSDATE(), %s, %s, 'TELEGRAM' ) "
        self.curs.execute(self.sql, data)
        self.db.commit()


########################################################################################################################

########################################################################################################################
#  전역 함수 처리(외부 에서 호출 할 때 쓰임)
class MYSQL(MariaDB):

    def selmysql(self, opt, data):
        try:
            result = ""
            MYSQL.conn(self)
            MYSQL.getcurs(self)

            #  print("정상적 으로 MariaDB에 연결 되었 습니다.")
            if   opt == "TEMP":
                MYSQL.tempmysql(self, data)
            elif opt == "TOKEN":
                result = MYSQL.tokenmysql(self, data)
            elif opt == "LOG":
                MYSQL.logmysql(self, data)

            MYSQL.closemysql(self)
            #  print("정상적 으로 MariaDB에 연결 해제 되었 습니다.")
            return result

        except Exception:
            Errlog.savelog('ERROR')
########################################################################################################################
