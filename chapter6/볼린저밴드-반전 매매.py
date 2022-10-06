import matplotlib.pyplot as plt
from Investar import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('SK하이닉스', '2018-11-01')
  
df['MA20'] = df['close'].rolling(window=20).mean() 
df['stddev'] = df['close'].rolling(window=20).std() 
df['upper'] = df['MA20'] + (df['stddev'] * 2)
df['lower'] = df['MA20'] - (df['stddev'] * 2)
df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower'])

#종가 고가 저가 거래량을 이용해 일중 강도 ||를 구한다.
df['II'] = (2*df['close']-df['high']-df['low'])/(df['high']-df['low'])*df['volume']
#21일간의 일중 강도 ||합을 21일간의 거래량 합으로 나누어 일종 강도율||%를 구한다.
df['IIP21'] = df['II'].rolling(window=21).sum()/df['volume'].rolling(window=21).sum()*100
df = df.dropna()

plt.figure(figsize=(9, 9))
plt.subplot(3, 1, 1)
plt.title('SK Hynix Bollinger Band(20 day, 2 std) - Reversals')
plt.plot(df.index, df['close'], 'b', label='Close')
plt.plot(df.index, df['upper'], 'r--', label ='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label ='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
for i in range(0, len(df.close)):
    #%b<0.05 21일 기준||%>0 매수 시점으로 빨간색 삼각형
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:   
        plt.plot(df.index.values[i], df.close.values[i], 'r^')
    #%b>0.95 21일 기준||%<0 매도 시점으로 파란색 삼각형
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0: 
        plt.plot(df.index.values[i], df.close.values[i], 'bv')

plt.legend(loc='best')
plt.subplot(3, 1, 2)
plt.plot(df.index, df['PB'], 'b', label='%b')
plt.grid(True)
plt.legend(loc='best')

plt.subplot(3, 1, 3)
#녹색 실선으로 21일 일중 강도율을 표시한다.
plt.bar(df.index, df['IIP21'], color='g', label='II% 21day')
for i in range(0, len(df.close)):
    #일중 강도율 그래프에 매수 시점을 빨간색 삼각형으로
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:   
        plt.plot(df.index.values[i], 0, 'r^')
    #일중 강도율 그래프에 매도 시점을 파란색 삼각형으로
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0: 
        plt.plot(df.index.values[i], 0, 'bv')
plt.grid(True)
plt.legend(loc='best')
plt.show()