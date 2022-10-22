import numpy as np
import matplotlib.pyplot as plt

#x값이 음수쪽으로 멀어지면 y값은 0에 가까워지고, x값이 양수쪽으로 멀어지면 y값은 1에 가까워진다.
def sigmoid(x):
    return 1 / (1 + np.exp(-x)) 

x = np.arange(-10, 10, 0.1)
y = sigmoid(x) 

plt.plot(x, y)
plt.title('sigmoid function')
plt.show()