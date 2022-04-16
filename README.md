# DEV_PYTHON_BOT
<hr/>
2022.04.11  
  
1.Telegram bot 생성.  

2.Errlog.py 생성  

  -logging 레벨 ERROR   
  -logging 파일 ./DEV_PYTHON_BOT_log.log 생성  
  -logging 파일형식  

  '[%(process)d | %(thread)d | %(levelname)s | %(filename)s:%(lineno)s] %(asctime)s: %(message)s'  

*mysql.py 생성  
  -현재 딱히 구현된건 없고 나중에  log관련 데이터 관리하는 테이블 생성예정
<hr/>
<hr/>
2022.04.16  
  
1.Errlog.py 수정  

  -logging 파일형식 변경

  '[%(process)d | %(thread)d | %(filename)s:%(lineno)s] %(asctime)s: %(message)s'  

2.mysql.py 수정  

  -SetMysql, CloseMysql 추가   
<hr/>
