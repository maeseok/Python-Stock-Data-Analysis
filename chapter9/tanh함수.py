import numpy as np
import matplotlib.pyplot as plt

def tanh(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))  

#-10 ~9.9까지 0.1간격의 소수
x = np.arange(-10, 10, 0.1) 
#이거 대신 np.tanh() 함수 사용해도 결과는 동일
y = tanh(x) 

plt.plot(x, y)
plt.title('tanh function')
plt.show()