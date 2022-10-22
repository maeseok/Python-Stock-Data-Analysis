import numpy as np
import matplotlib.pyplot as plt

def relu(x):
    #인수로 주어진 수 중에서 가장 큰 수를 반환한다.
    return np.maximum(0, x)

#-10 ~9.9까지 0.1 간격으로 이루어진 배열
x = np.arange(-10, 10, 0.1)
y = relu(x)

plt.plot(x, y)
plt.title('ReLU function')
plt.show()