from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
import matplotlib.pyplot as plt

df = pdr.get_data_yahoo('005930.KS', '2017-01-01')  # ①

plt.figure(figsize=(9, 6))
#2행 1열 영역에서 첫 번째 영역을 선택
plt.subplot(2, 1, 1)  # 
plt.title('Samsung Electronics (Yahoo Finance)')
#종가를 청록색 실선으로 표시
plt.plot(df.index, df['Close'], 'c', label='Close')  # 
#수정된 종가를 파란색 점선으로 표시
plt.plot(df.index, df['Adj Close'], 'b--', label='Adj Close')  # 
plt.legend(loc='best')
#2행 1열 영역에서 두 번째 영역을 선택
plt.subplot(2, 1, 2)  # 
#바 차트로 그림
plt.bar(df.index, df['Volume'], color='g', label='Volume')  # 
plt.legend(loc='best')
plt.show()