import matplotlib.pylab as plt
import tensorflow as tf

x_data = [1, 2, 3, 4, 5]
#y=1*x+1 값을 준비
y_data = [2, 3, 4, 5, 6]

#가중치를 임의 값 0.7로 초기화
w = tf.Variable(0.7)
#편향을 임의 값 0.7로 초기화
b = tf.Variable(0.7)
#학습률을 설정-> 너무 크면 비용이 커지는 오버슈팅 현상이 발생, 너무 작으면 시간이 너무 오래 걸린다.
learn_rate = 0.01

print(f'step|    w|    b| cost')
print(f'----|-----|-----|-----')

#1회부터 1100회까지 반복
for i in range(1, 1101): 
    #내부의 계산 과정을 tape에 기록해두면, 나중에 tape.gradient()함수를 이용해서 미분값을 구할 수 있다.
    with tf.GradientTape() as tape:
        #w*x+b로 가설을 정한다.
        hypothesis = w * x_data + b
        #손실 비용은 오차제곱평균으로 구한다.
        cost = tf.reduce_mean((hypothesis - y_data)**2) # tf.losses.mean_squared_error(y, y_hat)
    #w와 b에 대해 손실을 미분해서 dw, db를 구한다.
    dw, db = tape.gradient(cost, [w, b])
    #w에서 학습률*dw값을 빼서 w에 저장
    w.assign_sub(learn_rate * dw) # a = a - b
    b.assign_sub(learn_rate * db) 
    
    if i in [1, 3, 5, 10, 1000, 1100]:
        print(f"{i:4d}| {w.numpy():.2f}| {b.numpy():.2f}| {cost:.2f}")
        plt.figure(figsize=(7, 7))
        plt.title(f'[Step {i:d}]  h(x) = { w.numpy():.2f}x + {b.numpy():.2f}')
        plt.plot(x_data, y_data, 'o') # ⑥
        plt.plot(x_data, w * x_data + b, 'r', label='hypothesis') # ⑦
        plt.xlabel('x_data')
        plt.ylabel('y_data')
        plt.xlim(0, 6)
        plt.ylim(1, 7)
        plt.legend(loc='best')
        plt.show()
