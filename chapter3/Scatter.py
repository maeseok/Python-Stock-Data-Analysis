import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

#다우지수, 코스피 지수 시세 다운로드
dow = pdr.get_data_yahoo('^DJI', '2000-01-04')
kospi = pdr.get_data_yahoo('^KS11', '2000-01-04')

df = pd.DataFrame({'DOW': dow['Close'], 'KOSPI': kospi['Close']})
#nan값을 bfill 즉 뒤에 있는 값으로 바꿈, ffill은 앞에 있는 값으로 바꿈.
df = df.fillna(method='bfill')
df = df.fillna(method='ffill')

import matplotlib.pyplot as plt
plt.figure(figsize=(7, 7))
#산점도 함수(x,y,.으로 표시)
plt.scatter(df['DOW'], df['KOSPI'], marker='.')
plt.xlabel('Dow Jones Industrial Average')
plt.ylabel('KOSPI')
plt.show()

#통계 함수 제공
from scipy import stats
#(독립변수, 종속변수) -> 선형 회귀 모델 생성 = (기울기, y절편, r값, p값, 표준편차)
regr = stats.linregress(df['DOW'],df['KOSPI'])

#데이터프레임으로 상관계수 구하기
df.corr()
#시리즈로 상관계수 구하기
r_value = df['DOW'].corr(df['KOSPI'])
r_squard = r_value ** 2

