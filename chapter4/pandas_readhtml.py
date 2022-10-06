import pandas as pd
#xls이지만 원본이 html 형태이기에 read_html
df = pd.read_html('./상장법인목록.xls')[0]
#format으로 6자리 숫자형식으로 표현하되 빈 앞자릴 0으로 채우는 것
df['종목코드'] = df['종목코드'].map('{:06d}'.format)
df = df.sort_values(by="종목코드")
print(df)