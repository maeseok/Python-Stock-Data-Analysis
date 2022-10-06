import pandas as pd 

#시리즈 생성
s = pd.Series([0.0,3.6,2.0,5.8,4.2,8.0])

#시리즈의 인덱스 변경
s.index = pd.Index([0.0,1.2,1.8,3.0,3.6,4.8])
s.index.name = 'MY_IDX' #맨 위에 인덱스명 출력됨

#시리즈명 설정
s.name = 'MY_SERIES' #맨 뒤에 시리즈명 출력됨

#데이터 추가
s[5.9] = 5.5
#데이터 추가 (append)
ser = pd.Series([6.7,4.2],index=[6.8,8.0])
s= s.append(ser)

#인덱스와 데이터 출력
s.index[-1]
s.values[-1]
s.loc[8.0] #4.2
s.iloc[-1] #4.2 (시리즈로 반환)
s.values[:] # iloc와 비슷하지만 배열로 반환

#데이터 삭제
s.drop(8.0) #인덱스 8.0 라인 삭제
#시리즈 정보 보기
s.describe() #원소 개수, 평균, 표준편차, 최솟값, 제1~3 사분위수, 최댓값

import matplotlib.pyplot as plt
plt.title("ELLIOTT_WAVE")
plt.plot(s,'bs--') #시리즈를 bs--(푸른 사각형과 점선 형태)로 출력
plt.xticks(s.index) #x축의 눈금값을 s 시리즈의 인덱스값으로 설정
plt.yticks(s.values) #y축의 눈금값을 s 시리즈의 데이터값으로 출력
plt.grid(True)
plt.show()






print(s)