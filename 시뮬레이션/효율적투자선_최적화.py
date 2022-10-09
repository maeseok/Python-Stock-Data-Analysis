import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Analyzer

mk = Analyzer.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()
for s in stocks:
    df[s] = mk.get_daily_price(s, '2022-01-04', '2022-09-27')['close']

#4종목의 일간 변동률을 구한다.생성
daily_ret = df.pct_change()
#일간 변동률 평균*252 = 연간 수익률
annual_ret = daily_ret.mean() * 252
#일간 변동률의 공분산으로 구한다.
daily_cov = daily_ret.cov()
#일간 공분산*252 = 연간 공분산 
annual_cov = daily_cov * 252

port_ret = [] 
port_risk = [] 
port_weights = []
sharpe_ratio = []

#몬테카를로 시뮬레아션 - 많은 난수를 이용해 함수 값을 확률적으로 계산하는 것
for _ in range(20000): #반복 횟수를 사용할 일이 없으면 관습적으로 _로 표시
    #비중배열 생성
    weights = np.random.random(len(stocks)) 
    #4종목의 랜덤 숫자 합으로 나눠 4종목 비중의 합이 1이 되도록 조정 (총 4개 배열존재)
    weights /= np.sum(weights) 

    #비중 배열과 종목별 연간 수익률을 곱해 포트폴리오 전체 수익률을 구함.
    returns = np.dot(weights, annual_ret) 
    #연간 공분산 * 종목별 비중 * 종목별 비중의 전치를 루트 씌우면 리스크
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights))) 

    port_ret.append(returns) 
    port_risk.append(risk) 
    port_weights.append(weights)
    #수익률을 리스크로 나눈 값을 샤프 지수에 추가
    sharpe_ratio.append(returns/risk) 

portfolio = {'Returns': port_ret, 'Risk': port_risk, 'Sharpe': sharpe_ratio} 
for i, s in enumerate(stocks): 
    #종목(s)별로 4개의 배열을 순서대로 넣음
    portfolio[s] = [weight[i] for weight in port_weights] 
#데이터프레임에 저장
df = pd.DataFrame(portfolio)
#7개 모두 값 저장 -> 4 종목의 보유 비율에 따라 포트폴리오 20000개가 각기 다른 리스크와 예상 수익률 가짐
df = df[['Returns', 'Risk','Sharpe'] + [s for s in stocks]] 

#샤프 지수 큰 값 저장
max_sharpe = df.loc[df['Sharpe']==df['Sharpe'].max()]
#최저 위험 저장
min_risk = df.loc[df['Risk']==df['Risk'].min()]
print(max_sharpe)
print(min_risk)
#산점도 형태로 x = 위험 y = 수익으로 출력
#샤프 지수에 따라 컬러맵을 viridis로 표시하고 테두리는 검정(k)로 표시
df.plot.scatter(x='Risk', y='Returns', c='Sharpe', cmap='viridis',
    edgecolors='k', figsize=(11,7), grid=True)
#샤프 지수가 가장 큰 포트폴리오를 300 크기의 붉은 별로 표시
plt.scatter(x=max_sharpe['Risk'], y=max_sharpe['Returns'], c='r', 
    marker='*', s=300) 
#리스크가 제일 작은 포트폴리오를 200 크기의 붉은 x로 표시
plt.scatter(x=min_risk['Risk'], y=min_risk['Returns'], c='r', 
    marker='X', s=200)

#plt.title('Efficient Frontier') 
plt.title('Portfolio Optimization')
plt.xlabel('Risk') 
plt.ylabel('Expected Returns') 
plt.show()



#샤프 지수가 큰 포트폴리오 반환
