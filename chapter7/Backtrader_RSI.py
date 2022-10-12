from datetime import datetime
import backtrader as bt
import inspect
print(inspect.getfile(bt))


#bt.Strategy 클래스를 상속받아서 MyStrategy 클래스를 작성한다.
class MyStrategy(bt.Strategy):
    def __init__(self):
        #RSI 지표를 사용하려면 MyStrategy 클래스 생성자에서 RSI 지표로 사용할 변수를 지정
        self.rsi = bt.indicators.RSI(self.data.close)
    # next는 데이터와 지표를 만족시키는 최소 주기마다 자동 호출(시장 참여x+RSI 30미만 = 매수, 시장 참여o+RSI 70초과하면 매도)
    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()

#데이터를 취합하고 백테스트 또는 라이브 트레이딩을 실행한 뒤 그 결과를 출력한느 기능을 담당한다.
cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
#엔씨소프트의 종가 데이터를 야후 파이낸스 데이터를 이용해서 취합
data = bt.feeds.YahooFinanceData(dataname='036570.KS',
    fromdate=datetime(2017, 1, 1), todate=datetime(2019, 12, 1))
cerebro.adddata(data)
#초기 투자금을 천만 원으로 설정한다.
cerebro.broker.setcash(10000000)
#매매 단위는 30주로 설정한다. 보유 현금에 비해 총 매수 금액이 크면 매수가 이루어지지 않는다.
cerebro.addsizer(bt.sizers.SizerFix, stake=30)

print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
#Cerebro 클래스로 백테스트를 실행한다.
cerebro.run()
print(f'Final Portfolio Value   : {cerebro.broker.getvalue():,.0f} KRW')
#백테스트 결과를 차트로 출력한다.
cerebro.plot()