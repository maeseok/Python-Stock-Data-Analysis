import numpy as np
import matplotlib.pyplot as plt

#x값이 0보다 작거나 값으면 0, 아니면 1을 반환
def stepfunc(x):
    return np.where(x <= 0, 0, 1)

#x값으로 -10부터 9.9까지 0.1 간격의 소수로 이루어진 배열을 준비
x = np.arange(-10, 10, 0.1)
y = stepfunc(x)

plt.plot(x, y)
plt.title('step function')
plt.show()