import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
#패킷 헤더의 브라우저 정보를 추가 - 없으면 봇으로 간주하여 네이버에서 차단
html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
#url과 파싱방식을 념겨줌
bs = BeautifulSoup(html, 'lxml')
pgrr = bs.find('td', class_='pgRR')
#전체 텍스트를 보기 좋게 출력
print(pgrr.prettify())
#텍스트 부분만 출력
print(pgrr.text)
# 문자열을 리스트로 얻어서 전체 페이지 수를 확인
s = str(pgrr.a['href']).split('=')
last_page = s[-1]  





#전체 페이지 읽어오기
df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'  
for page in range(1, int(last_page)+1):
    url = '{}&page={}'.format(sise_url, page)  
    html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
    # read_html 함수로 읽은 한 페이지 분량의 데이터프레임을 df 객체에 추가한다.
    df = df.append(pd.read_html(html, header=0)[0])

# 차트 출력을 위해 데이터프레임 가공하기
df = df.dropna() #값이 빠진 행은 제거
df = df.iloc[0:30]  #30개의 데이터만 사용
df = df.sort_values(by='날짜')  #날짜기준으로 오름차순으로 변경

# 날짜, 종가 컬럼으로 차트 그리기
plt.title('Celltrion (close)')
plt.xticks(rotation=45)  #x축 레이블의 날짜가 겹쳐서 보기에 어려우므료 90도 회전하여 표시
plt.plot(df['날짜'], df['종가'], 'co-')  #청록색으로 각 좌표를 실선으로 연결
plt.grid(color='gray', linestyle='--')
plt.show()