import pandas as pd
from bs4 import BeautifulSoup
import pymysql, calendar, time, json
import requests
import pwd
from datetime import datetime
from threading import Timer

PWD = pwd.password()

class DBUpdater:  
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        #charset='utf-8'로 꼭 설정
        self.conn = pymysql.connect(host='localhost', user='root',
            password=PWD, db='INVESTAR', charset='utf8')
        
        with self.conn.cursor() as curs:
            #존재하는 테이블이 있을 때 경고만 뜨고 종료가 안되게 설정
            sql = """
            CREATE TABLE IF NOT EXISTS company_info (
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (code))
            """
            curs.execute(sql)
            sql = """
            CREATE TABLE IF NOT EXISTS daily_price (
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
            """
            curs.execute(sql)
        self.conn.commit()
        self.codes = dict()
    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close() 
     
    def read_krx_code(self):
        """KRX로부터 상장기업 목록 파일을 읽어와서 데이터프레임으로 반환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method='\
            'download&searchType=13'
        krx = pd.read_html(url, header=0)[0]
        #종목코드 회사명만 남긴다.
        krx = krx[['종목코드', '회사명']]
        #한글 칼럼을 영문으로 변경한다.
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})
        #종목 코드 형식을 6자리 채우게 만든다.
        krx.code = krx.code.map('{:06d}'.format)
        return krx
    
    def update_comp_info(self):
        """종목코드를 company_info 테이블에 업데이트 한 후 딕셔너리에 저장"""
        sql = "SELECT * FROM company_info"
        #company_info 테이블을 read_sql로 읽는다.
        df = pd.read_sql(sql, self.conn)
        #df를 이용해서 새로운 code 딕셔너리를 만든다.
        for idx in range(len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx]
                    
        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM company_info"
            curs.execute(sql)
            #SELECT max 이용하여 DB에서 가장 최근 업데이트 날짜를 가져온다.
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')
            #날짜가 없거나 오늘 날짜가 아니면 새로 업데이트
            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                #KRX 상장기업 목록 파일을 읽어서 krx 데이터프레임에 저장
                krx = self.read_krx_code()
                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]
                    #REPLACE INTO 문을 이용해서 DB에 저장 (INSERT INTO문 사용 시 오류 -> INSER+UPDATE=UPSERT라고 부름 = REPLACE INTO)                
                    sql = f"REPLACE INTO company_info (code, company, last"\
                        f"_update) VALUES ('{code}', '{company}', '{today}')"
                    curs.execute(sql)
                    #딕셔너리에 키-값으로 종목코드와 회사명을 추가한다.
                    self.codes[code] = company
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] #{idx+1:04d} REPLACE INTO company_info "\
                        f"VALUES ({code}, {company}, {today})")
                self.conn.commit()
                print('')              

    def read_naver(self, code, company, pages_to_fetch):
        """네이버에서 주식 시세를 읽어서 데이터프레임으로 반환"""
        try:
            url = f"http://finance.naver.com/item/sise_day.nhn?code={code}"
            html = BeautifulSoup(requests.get(url,
                headers={'User-agent': 'Mozilla/5.0'}).text, "lxml")
            pgrr = html.find("td", class_="pgRR")
            if pgrr is None:
                return None
            s = str(pgrr.a["href"]).split('=')
            #일별 시세의 마지막 페이지를 구한다.
            lastpage = s[-1] 
            df = pd.DataFrame()
            #설정 파일에 설정된 페이지 수와 lastpage 중에서 작은 것을 택한다.
            pages = min(int(lastpage), pages_to_fetch)
            for page in range(1, pages + 1):
                pg_url = '{}&page={}'.format(url, page)
                #일별 시세 페이지를 읽어서 데이터프레임에 추가한다.
                df = df.append(pd.read_html(requests.get(pg_url,
                headers={'User-agent': 'Mozilla/5.0'}).text)[0])    
                tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                print('[{}] {} ({}) : {:04d}/{:04d} pages are downloading...'.
                    format(tmnow, company, code, page, pages), end="\r")
            #한글 컬럼명을 영문으로 변경한다.
            df = df.rename(columns={'날짜':'date','종가':'close','전일비':'diff'
                ,'시가':'open','고가':'high','저가':'low','거래량':'volume'})
            #연-월-일 형식으로 변경한다.
            df['date'] = df['date'].replace('.', '-')
            df = df.dropna()
            #BIGINT형으로 지정한 칼럼들의 데이터형을 int형으로 변경한다.
            df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close',
                'diff', 'open', 'high', 'low', 'volume']].astype(int)
            #원하는 순서로 칼럼을 재조합하여 데이터프레임을 만든다.
            df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']]
        except Exception as e:
            print('Exception occured :', str(e))
            return None
        return df

    def replace_into_db(self, df, num, code, company):
        """네이버에서 읽어온 주식 시세를 DB에 REPLACE"""
        #to_sql 사용시 종목별로 테이블 구성해야 하고 데이터를 저장할 때 기존 테이블을 전체적으로 교체하기에 비효율적
        #daily_price 테이블 하나에 저장하여 테이블 크기가 커져서 성능 면에서 바람직하지 않다.
        with self.conn.cursor() as curs:
            #인수로 넘겨받은 데이터프레임을 듀플로 순회처리
            for r in df.itertuples():
                #daily_price 업데이트
                sql = f"REPLACE INTO daily_price VALUES ('{code}', "\
                    f"'{r.date}', {r.open}, {r.high}, {r.low}, {r.close}, "\
                    f"{r.diff}, {r.volume})"
                curs.execute(sql)
            #commit하여 마리아디비에 반영
            self.conn.commit()
            print('[{}] #{:04d} {} ({}) : {} rows > REPLACE INTO daily_'\
                'price [OK]'.format(datetime.now().strftime('%Y-%m-%d'\
                ' %H:%M'), num+1, company, code, len(df)))

    def update_daily_price(self, pages_to_fetch):
        """KRX 상장법인의 주식 시세를 네이버로부터 읽어서 DB에 업데이트"""  
        #self.codes 딕셔너리에 저장된 모든 종목코드에 대해 순회처리
        for idx, code in enumerate(self.codes):
            #read_naver 이용하여 종목코드에 대한 일별 시세 데이터 프레임을 구한다.
            df = self.read_naver(code, self.codes[code], pages_to_fetch)
            if df is None:
                continue
            #구해지면 replace_info_db() 메서드로 DB에 저장한다.
            self.replace_into_db(df, idx, code, self.codes[code])            

    def execute_daily(self):
        """실행 즉시 및 매일 오후 다섯시에 daily_price 테이블 업데이트"""
        #메서드를 호출하여 상장 법인 목록을 DB에 업데이트
        self.update_comp_info()
        
        try:
            #현재 파일이 있는 디렉터리에서 config.json 파일을 읽기 모드로 연다.
            with open('config.json', 'r') as in_file:
                config = json.load(in_file)
                #파일 있으면 pages_to_fetcj값을 읽어서 저장
                pages_to_fetch = config['pages_to_fetch']
        except FileNotFoundError:
            with open('config.json', 'w') as out_file:
                #파일 없으면 초기값 100으로 설정
                pages_to_fetch = 100 
                config = {'pages_to_fetch': 1}
                json.dump(config, out_file)
        #pages_to_fatch로 메서드 호출
        self.update_daily_price(pages_to_fetch)

        tmnow = datetime.now()
        #이번 달 마지막 날을 구해 다음 날 오후 5시를 계산하는 데 사용
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]
        if tmnow.month == 12 and tmnow.day == lastday:
            tmnext = tmnow.replace(year=tmnow.year+1, month=1, day=1,
                hour=17, minute=0, second=0)
        elif tmnow.day == lastday:
            tmnext = tmnow.replace(month=tmnow.month+1, day=1, hour=17,
                minute=0, second=0)
        else:
            tmnext = tmnow.replace(day=tmnow.day+1, hour=17, minute=0,
                second=0)   
        tmdiff = tmnext - tmnow
        secs = tmdiff.seconds
        #다음 날 오후 5시에 excute_daily 메서드를 실행하는 타이머 객체를 생성
        t = Timer(secs, self.execute_daily)
        print("Waiting for next update ({}) ... ".format(tmnext.strftime
            ('%Y-%m-%d %H:%M')))
        t.start()

if __name__ == '__main__':
    #단독으로 실행 시 DBUpdater 객체를 생성
    dbu = DBUpdater()
    #업데이트 함수 실행
    dbu.execute_daily()