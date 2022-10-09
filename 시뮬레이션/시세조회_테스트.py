import matplotlib.pyplot as plt
#Investar 패키지는 실습용으로 제작하는 패키지
import Analyzer  # ①

#MarketDB클래스로부터 mk객체를 생성한다.
mk = Analyzer.MarketDB()  # ②
#사용하려면 마리아디비 설치 후 DBUpdater.py를 통해 일별 시세 데이터를 업데이트해야함
df = mk.get_daily_price('000000', '2021-03-10', '2022-03-30')  # ③

plt.figure(figsize=(9, 6))
#2행 1열 영역에서 첫 번째 영역을 선택
plt.subplot(2, 1, 1)
plt.title('Kakao (Investar Data)')
#종가를 청록색 실선으로 표시
plt.plot(df.index, df['close'], 'c', label='Close')  # ④
plt.legend(loc='best')
#2행 1열 영역에서 두 번째 영역을 선택
plt.subplot(2, 1, 2)
#바 차트로 그림
plt.bar(df.index, df['volume'], color='g', label='Volume')
plt.legend(loc='best')
plt.show()