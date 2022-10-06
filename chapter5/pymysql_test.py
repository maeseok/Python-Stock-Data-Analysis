import pymysql

#connect 함수 이용하여 connection 객체를 생성
connection = pymysql.connect(host='localhost', port=3306, db='INVESTAR', 
    user='root', passwd='endrk1313', autocommit=True)  

#cursor 함수 사용해 cursor 생성
cursor = connection.cursor()
#execute 사용해 SELECT문 실행
cursor.execute("SELECT VERSION();")
#실행 결과를 튜플로 받는다.
result = cursor.fetchone()

print ("MariaDB version : {}".format(result))

connection.close()