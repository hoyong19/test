import openpyxl
import schedule
import pyupbit
import ccxt
import time, datetime
from currency_converter import CurrencyConverter


currency_rate = CurrencyConverter('http://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')
server = 1 # 0: local / 1 : servers

# 새로운 워크북 만들기
wb = openpyxl.Workbook()
# 현재 시트 선택
sheet = wb.active
# 헤더 추가하기
sheet.append(["Month","Day","Hour","Min","Upbit(₩)", "Binance($)", "Currency", "Kimch P"])


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
    BinanXrp_k = BinanXrp_d * currency_rate.convert(1,'USD','KRW')
    Kimch_P = UpbitXrp/BinanXrp_k*100-100
    now = time.localtime()

    if server == 1 :
        Hour = now.tm_hour + 9
        if Hour >= 24 :
            Hour = Hour - 24
            Day = now.tm_mday +1

    #print(str(int(datetime.datetime.now().timestamp())),str(UpbitXrp), str(BinanXrp_d), str(currency_rate.convert(1,'USD','KRW')), str(Kimch_P))
    sheet.append([str(now.tm_mon),str(Day),str(Hour),str(now.tm_min),str(UpbitXrp), str(BinanXrp_d), str(currency_rate.convert(1,'USD','KRW')), str(Kimch_P)]) 
    wb.save('kimp.xlsx')

schedule.every(1).minutes.do(makeTS_01)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        time.sleep(1)

