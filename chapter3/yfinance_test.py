from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
#get_data_yahoo(조회할 주식 종목 [, start=조회 시작일],[ end = 조회 종료일])
sec = pdr.get_data_yahoo('005930.KS',start='2018-05-04')
msft = pdr.get_data_yahoo('MSFT',start='2018-05-04')

#기존 msft에서 거래량을 제외함
tmp_msft = msft.drop(columns='Volume')
#인덱스 정보 확인
sec.index
# 칼럼 정보 확인
sec.columns

#plot(x,y, 마커 형태 [,label='Label])
import matplotlib.pyplot as plt
plt.plot(sec.index,sec.Close,'b',label='Samsung Electronics')
plt.plot(msft.index,msft.Close,'r--',label='Microsoft')
plt.legend(loc='best')
plt.show()

#일간 변동률로 주가 비교하기 (오늘종가-어제종가)/어제종가 * 100
type(sec['Close']) #시리즈
sec['Close'].shift(1) #전체 데이터가 n행씩 뒤로 이동한다.
sec_dpc = (sec['Close']/sec['Close'].shift(1)-1)*100
sec_dpc.head()
sec_dpc.iloc[0]=0 #첫번째 값을 0으로 변경
sec_dpc.head()

#주가 일간 변동률 히스토그램 : 데이터값들에 대한 구간별 빈도수를 막대 형태로 표현
#구간 수를 빈스라고 하는데 hist()함수에서 사용되는 기본값은 10이다.
sec_dpc = (sec['Close']-sec['Close'].shift(1))/sec['Close'].shift(1) *100
sec_dpc.iloc[0]=0
#히스토그램 함수 (좌우 각 5개씩)
plt.hist(sec_dpc,bins=10)
plt.grid(True)
plt.show() #급첨 분포와 팻 테일을 나타냄 150p

#일간 변동율 누적곱 구하기 cumprod() 함수 이용
sec_dpc_cp = ((100+sec_dpc)/100).cumprod()*100-100
print(sec_dpc_cp) #4년동안 1.3% 이익봄
