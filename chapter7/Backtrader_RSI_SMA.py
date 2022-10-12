import backtrader as bt
from datetime import datetime

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None        
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)
    #MyStrategy 클래스에 notify_order 추가됨, 주문 상태에 변화가 있을 때마다 실행 (완료,취소,마진,거절 등)
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        #주문 상태 완료이면 매수인지 매도인지 확인하여 상세 주문 정보를 출력
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY  : 주가 {order.executed.price:,.0f}, '
                    f'수량 {order.executed.size:,.0f}, '
                    f'수수료 {order.executed.comm:,.0f}, '        
                    f'자산 {cerebro.broker.getvalue():,.0f}') 
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else: 
                self.log(f'SELL : 주가 {order.executed.price:,.0f}, '
                    f'수량 {order.executed.size:,.0f}, '
                    f'수수료 {order.executed.comm:,.0f}, '
                    f'자산 {cerebro.broker.getvalue():,.0f}') 
            self.bar_executed = len(self)
        elif order.status in [order.Canceled]:
            self.log('ORDER CANCELD')
        elif order.status in [order.Margin]:
            self.log('ORDER MARGIN')
        elif order.status in [order.Rejected]:
            self.log('ORDER REJECTED')
        self.order = None

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()
    #log() 메서드는 텍스트 메시지를 인수로 받아서 셸 화면에 주문 일자와 함께 출력하는 역할
    def log(self, txt, dt=None):
        dt = self.datas[0].datetime.date(0)
        print(f'[{dt.isoformat()}] {txt}')

cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
data = bt.feeds.YahooFinanceData(dataname='036570.KS',
    fromdate=datetime(2017, 1, 1), todate=datetime(2019, 12, 1))
cerebro.adddata(data)
cerebro.broker.setcash(10000000)
#수수료는 매수나 매도 발생할 때마다 차감 - 보통 매수 0.14 매도 0.14 차감
cerebro.broker.setcommission(commission=0.0014)
#매매 주문을 적용할 주식 수 (가진 돈의 90% + 수수료)
cerebro.addsizer(bt.sizers.PercentSizer, percents=90)

print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()
print(f'Final Portfolio Value   : {cerebro.broker.getvalue():,.0f} KRW')
#캔들스틱 차트로 표시
cerebro.plot(style='candlestick')