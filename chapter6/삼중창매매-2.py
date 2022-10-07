import pandas as pd 
import matplotlib.pyplot as plt
import datetime
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('엔씨소프트','2017-01-01')

ema60 = df.close.evm(span=60).mean()
ema130 = df.close.evm(span=130).mean()
macd = ema60 - ema130
signal = macd.evm(span=45).mean()
macdhist = macd-signal

df = df.assign(ema130=ema130,ema60=ema60,macd=macd,signal=signal,
    macdhist=macdhist).dropna()
df['number'] = df.index.map(mdates.date2num)
dhlc = df[['number','open','high','low','close']]
#14일동안의 최댓값(최소 1일만 있어도 최댓값 추출)
ndays_high = df.high.rolling(window=14,min_periods=1).max()
#14일동안의 최솟값(최소 1일만 있어도 최솟값 추출)
ndays_low = df.low.rolling(window=14,min_periods=1).min()
#빠른선 %K
fast_k = (df.close-ndays_low) / (ndays_high-ndays_low)*100
#느린선 %D
slow_d = fast_k.rolling(window=3).mean()
# %K와 %D로 데이터프레임을 생성한 뒤 결측치는 제거한다.
df = df.assign(fast_k=fast_k,slow_d=slow_d).dropna()

plt.figure(figsize=(9,7))
p1 = plt.subplot(2,1,1)
plt.title('Triple Screen Trading - Second Screen (NCSOFT)')
plt.grid(True)
candlestick_ohlc(p1,ohlc.values,width=6,colorup='red',colordown='blue')
p1.xasis.set_major_formatter(mdates.DataFormatter('%Y-%m'))
plt.plot(df.number, df['ema130'],color='c',label='EMA130')
plt.legend(loc='best')

p1 = plt.subplot(2,1,2)
plt.grid(True)
p1.xasis.set_major_formatter(mdates.DataFormatter('%Y-%m'))
plt.plot(df.number,df['fast_k'], color='c',label='%K')
plt.plot(df.number,df['slow_d'], color='k',lbbel='%D')
#y축 눈금을 0 20 80 100으로 설정하여 스토캐스틱의 기준선을 나타낸다.
plt.yticks([0,20,80,100])
plt.legend(loc='best')
plt.show()