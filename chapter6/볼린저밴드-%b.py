import matplotlib.pyplot as plt
from Investar import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('NAVER', '2019-01-02')

#20개 종가의 평균을 구함  
df['MA20'] = df['close'].rolling(window=20).mean()  
#표준편차
df['stddev'] = df['close'].rolling(window=20).std()
#상단 볼린저 밴드  
df['upper'] = df['MA20'] + (df['stddev'] * 2)   
#하단 볼린저 밴드
df['lower'] = df['MA20'] - (df['stddev'] * 2)
#볼린저 밴드 지표값
df['PB'] = (df['close']-df['lower'])/(df['upper']-df['lower'])  
#19번까지 NaN이라서 20부터 사용
df = df[19:] 


plt.figure(figsize=(9, 8))
plt.subplot(2,1,1)
#종가를 y좌표로 설정해 파란색 실선으로 표시
plt.plot(df.index, df['close'], color='#0000ff', label='Close') 
#상단 볼린저 밴드값을 y좌표로 설정해 검은 실선으로 표시
plt.plot(df.index, df['upper'], 'r--', label = 'Upper band')  
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label = 'Lower band')
#상단 볼린저 밴드와 하단 볼린저 밴드 사이를 회색으로 칠한다.
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')  # ⑧ 
plt.title('NAVER Bollinger Band (20 day, 2 std)')
plt.legend(loc='best')

plt.subplot(2,1,2)
#y좌표로 %B 설정 후 파란 실선으로 표시 
plt.plot(df.index,df['PB'],color='b',label='%B')
#상단1 중간 0.5 하단 0 을 기준으로 주가가 어디에있는지 보여줌
plt.grid(True)
plt.legend(loc='best')
plt.show()