from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import numpy as np
import matplotlib.pyplot as plt
import Analyzer

mk = Analyzer.MarketDB()
#데이터 가져오기
raw_df = mk.get_daily_price('삼성전자', '2018-05-04', '2022-10-18')
window_size = 10 
data_size = 5

def MinMaxScaler(data):
    """최솟값과 최댓값을 이용하여 0 ~ 1 값으로 변환"""
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    # 0으로 나누기 에러가 발생하지 않도록 매우 작은 값(1e-7)을 더해서 나눔
    return numerator / (denominator + 1e-7)

dfx = raw_df[['open','high','low','volume', 'close']]
#가격 정보를 0~1 사잇값으로 변환
dfx = MinMaxScaler(dfx)
dfy = dfx[['close']]

x = dfx.values.tolist()
y = dfy.values.tolist()

data_x = []
data_y = []
for i in range(len(y) - window_size):
    _x = x[i : i + window_size] # 다음 날 종가(i+windows_size)는 포함되지 않음
    _y = y[i + window_size]     # 다음 날 종가
    data_x.append(_x)
    data_y.append(_y)
print(_x, "->", _y)

#데이터 분리
train_size = int(len(data_y) * 0.7)
train_x = np.array(data_x[0 : train_size])
train_y = np.array(data_y[0 : train_size])

test_size = len(data_y) - train_size
test_x = np.array(data_x[train_size : len(data_x)])
test_y = np.array(data_y[train_size : len(data_y)])

# 모델 객체 생성
model = Sequential()
# (10,5) 입력 형태 가지는 LSTM층을 추가한다. 전체 개수는 10개이고, relu를 사용한다.
model.add(LSTM(units=10, activation='relu', return_sequences=True, input_shape=(window_size, data_size)))
# 입력값의 일부분을 선택해서 그 값을 0으로 치환하여 다음층으로 출력한다.
model.add(Dropout(0.1))
model.add(LSTM(units=10, activation='relu'))
model.add(Dropout(0.1))
#유닛이 하나인 출력층을 추가한다.
model.add(Dense(units=1))
model.summary()

#최적화 도구는 adam을 사용하고 손실 함수는 평균 제곱 오차(MSE)를 사용한다.
model.compile(optimizer='adam', loss='mean_squared_error')
#훈련용 데이터셋으로 모델을 학습시킨다. epochs는 전체 데이터셋에 대한 학습 횟수이고, batch_size는 한 번에 제공되는 훈련 데이터 개수다.
model.fit(train_x, train_y, epochs=60, batch_size=30)
#테스트 데이터셋을 이용하여 예측치 데이터셋을 생성한다.
pred_y = model.predict(test_x)

# Visualising the results
plt.figure()
plt.plot(test_y, color='red', label='real SEC stock price')
plt.plot(pred_y, color='blue', label='predicted SEC stock price')
plt.title('SEC stock price prediction')
plt.xlabel('time')
plt.ylabel('stock price')
plt.legend()
plt.show()

# raw_df.close[-1] : dfy.close[-1] = x : pred_y[-1]
print("Tomorrow's SEC price :", raw_df.close[-1] * pred_y[-1] / dfy.close[-1], 'KRW')
