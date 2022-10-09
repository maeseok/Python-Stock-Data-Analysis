import matplotlib.pyplot as plt
import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('카카오', '2022-01-02')
  
df['MA20'] = df['close'].rolling(window=20).mean() 
df['stddev'] = df['close'].rolling(window=20).std() 
df['upper'] = df['MA20'] + (df['stddev'] * 2)
df['lower'] = df['MA20'] - (df['stddev'] * 2)
df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower'])
#고가+저가+종가의 합을 나눠서 중심가격 구함
df['TP'] = (df['high'] + df['low'] + df['close']) / 3
df['PMF'] = 0 #긍정 현금 흐름
df['NMF'] = 0 #부정 현금 흐름
#0부터 종가개수-2까지
for i in range(len(df.close)-1):
    #i+1이 중심가격 크면 중심가격*거래량 -> 긍정적현금흐름에 저장, 부정은 0
    if df.TP.values[i] < df.TP.values[i+1]:
        df.PMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
        df.NMF.values[i+1] = 0
    else:
        df.NMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
        df.PMF.values[i+1] = 0
#10일 긍정적 현금 흐름 합을 10일 부정적 현금 흐름 합으로 나눈 결과 = 현금흐름비율 저장
df['MFR'] = df.PMF.rolling(window=10).sum() / df.NMF.rolling(window=10).sum()
#10일 기준 현금흐름지수를 계산한 결과를 MFI10에 저장
df['MFI10'] = 100 - 100 / (1 + df['MFR'])
df = df[19:]

plt.figure(figsize=(9, 8))
plt.subplot(2, 1, 1)
plt.title('NAVER Bollinger Band(20 day, 2 std) - Trend Following')
plt.plot(df.index, df['close'], color='#0000ff', label='Close')
plt.plot(df.index, df['upper'], 'r--', label ='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label ='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
for i in range(len(df.close)):
    #%b>0.8, 10일 기준 MFI>80면 첫 번째 그래프의 종가 위치에 빨간색 삼각형 표시
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:       
        plt.plot(df.index.values[i], df.close.values[i], 'r^') 
    #%b<0.2, 10일 기준 MFI<20면 첫 번째 그래프의 종가 위치에 파란색 삼각형 표시
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:     
        plt.plot(df.index.values[i], df.close.values[i], 'bv')
plt.legend(loc='best')

plt.subplot(2, 1, 2)
#MFI와 비교하기 쉽게 %b*100을 곱해서 푸른색 실선으로 표시
plt.plot(df.index, df['PB'] * 100, 'b', label='%B x 100')
#10일 기준 MFI를 녹색의 점선으로 표시
plt.plot(df.index, df['MFI10'], 'g--', label='MFI(10 day)')
#y눈금 -20~120까지 20단위로 표시
plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120])                  
for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
        plt.plot(df.index.values[i], 0, 'bv')
plt.grid(True)
plt.legend(loc='best')
plt.show();   