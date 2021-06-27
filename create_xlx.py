import openpyxl
import schedule
import pyupbit
import ccxt
from datetime import datetime
from datetime import date
import time
import requests
from bs4 import BeautifulSoup


# 새로운 워크북 만들기
wb = openpyxl.Workbook()
# 현재 시트 선택
sheet = wb.active
# 헤더 추가하기
sheet.append(["time","Upbit(₩)", "Binance($)", "Binance(₩)", "Currency", "Kimch P"])

def get_currency_exchange_rate(pair1, pair2):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'text/html; charset=utf-8'
    }

    response = requests.get("https://kr.investing.com/currencies/{}-{}".format(pair1, pair2), headers=headers)
    content = BeautifulSoup(response.content, 'html.parser')
    containers = content.find('span', {'id': 'last_last'})
    currnency = containers.text
    currnency = currnency.replace(',', '')
    currnency = float(currnency)
    return currnency

#Upbit 가격 XRP/won
def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

#Binance 가격 XRP/$
def get_binance_xrp():

    binance = ccxt.binance()
    ticker = binance.fetch_ticker('XRP/USDT')
    return ticker['close']

def makeTS_01():
    UpbitXrp = get_current_price("KRW-XRP") 
    BinanXrp_d = get_binance_xrp()
    Current_Exchange_rate =get_currency_exchange_rate('usd', 'krw')
    BinanXrp_k = BinanXrp_d * Current_Exchange_rate
    Kimch_P = UpbitXrp/BinanXrp_k*100-100
    ex_datetime = datetime.now()

    tday = date.today()
    tday_s = tday.strftime('%b-%d')
    new_filename = 'xrp_' + tday_s + '.xlsx'

    #print(now)
    #print(str(int(datetime.datetime.now().timestamp())),str(UpbitXrp), str(BinanXrp_d), str(currency_rate.convert(1,'USD','KRW')), str(Kimch_P))
    #sheet.append([str(now.tm_mon),str(now.tm_mday),str(now.tm_hour),str(now.tm_min),str(UpbitXrp), str(BinanXrp_d), str(BinanXrp_k), str(Current_Exchange_rate), str(Kimch_P)]) 
    sheet.append([ex_datetime,UpbitXrp, BinanXrp_d, BinanXrp_k, Current_Exchange_rate, Kimch_P])
    wb.save(new_filename)
    wb.close()


makeTS_01()
schedule.every(1).minutes.do(makeTS_01)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        time.sleep(1)

