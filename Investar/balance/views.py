from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_data(symbol):
    url = 'http://finance.naver.com/item/sise.nhn?code={}'.format(symbol)
    with urlopen(url) as doc:
        soup = BeautifulSoup(doc, "lxml", from_encoding="euc-kr")
        #id가 nowVal인 strong 태그를 찾는다.
        cur_price = soup.find('strong', id='_nowVal')
        cur_rate = soup.find('strong', id='_rate')
        #tite 태그를 찾는다.
        stock = soup.find('title')
        #콜론 기준으로 분리하여 종목명 구하고 좌우 공백 없애줌
        stock_name = stock.text.split(':')[0].strip()
        return cur_price.text, cur_rate.text.strip(), stock_name

def main_view(request):
    querydict = request.GET.copy()
    #GET 방식으로 넘어온 값 리스트 형태로 저장
    mylist = querydict.lists()
    rows = []
    total = 0

    for x in mylist:
        #mylist의 종목 코드로 get_data 함수 호출 후 값 저장
        cur_price, cur_rate, stock_name = get_data(x[0])      
        price = cur_price.replace(',', '')
        #종목수를 int형으로 변환 및 천자리마다 , 표시
        stock_count = format(int(x[1][0]), ',')
        sum = int(price) * int(x[1][0])
        stock_sum = format(sum, ',')
        #얻은 값들 rows에 추가   
        rows.append([stock_name, x[0], cur_price, stock_count, cur_rate,
            stock_sum])
        #평가금액은 주식수로 곱한 뒤 todal 변수에 저장
        total = total + int(price) * int(x[1][0])

    total_amount = format(total, ',')
    #balance.html에 전달할 값들을 딕셔너리 형태로 저장 
    values = {'rows' : rows, 'total' : total_amount}
    #값을 보내줌
    return render(request, 'balance.html', values)