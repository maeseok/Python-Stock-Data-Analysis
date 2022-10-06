from pandas_datareader import data as pdr
import yfinance as yf 
yf.pdr_override()
import matplotlib.pyplot as plt 

#코스피 지수 데이터 다운로드
kospi = pdr.get_data_yahoo('^KS11','2004-01-04')

#1년 동안의 개장일을 252일로 설정
window = 252
#KOSPI 종가 칼럼에서 1년 기간 단위로 최고치 peak를 구한다. (데이터 최소 개수 지정)
peak = kospi['Adj Close'].rolling(window, min_periods=1).max()
#최고치 대비 현재 KOSPI 종가가 얼마나 하락했는지 구한다.
drawdown = kospi['Adj Close']/peak
#1년 기간 단위로 최저치 max_dd를 구한다. 마이너스값이기 때문에 최저치가 바로 최대 손실 낙폭이 된다.
max_dd = drawdown.rolling(window, min_periods=1).min()

#정확한 MDD 값
max_dd.min()
#MDD를 기록한 기간 구하기 (위에서 나온 값)
max_dd[max_dd==-0.5453664915127007]

plt.figure(figsize=(9,7))
plt.subplot(211)
kospi['Close'].plot(label='KOSPI',title='KOSPI MDD',grid=True,legend=True)
plt.subplot(212)
drawdown.plot(c='blue',label='KOSPI DD',grid=True,legend=True)
max_dd.plot(c='red',label='KOSPI DD', grid=True, legend=True)
plt.show()