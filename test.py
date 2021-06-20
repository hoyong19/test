import pyupbit
import requests
import ccxt
import time
import schedule

from currency_converter import CurrencyConverter


currency_rate = CurrencyConverter('http://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')
myToken_m = ""

KimPMin = 3.5
KimPMax = 5.5
NoOfContToSnd = 851
UpbitTransfFee = 1
UpbitFee = 0.0005
BinanTransfFee = 0.25
BinaFee_M = 0.0001
BinaFee_T = 0.0005


#Upbit 가격 XRP/won
def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

#Binance 가격 XRP/$
def get_binance_xrp():

    binance = ccxt.binance()
    ticker = binance.fetch_ticker('XRP/USDT')
    return ticker['close']

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)

def print_message_m():
    UpbitXrp = get_current_price("KRW-XRP")
    BinanXrp_d = get_binance_xrp()
    BinanXrp_k = BinanXrp_d * currency_rate.convert(1,'USD','KRW')
    NoOfXRP = (10000000/UpbitXrp)*(1-UpbitFee-BinaFee_M) - UpbitTransfFee
    NoOfCont = NoOfXRP * BinanXrp_d / 10
    NoOfXrpToSnd = (NoOfContToSnd * 10 / BinanXrp_d)*(1-BinaFee_T) - BinanTransfFee
    Revenu = NoOfXrpToSnd * UpbitXrp - 10000000
    Kimch_P = UpbitXrp/BinanXrp_k*100-100
    now = time.localtime()

    print("Investing.com 현재 환율 :",currency_rate.convert(1,'USD','KRW'))    # 환율
    print("김프 %:", Kimch_P )    # 환율
    print("Upbit XRP :", UpbitXrp)                      # KRW-XRP 조회
    print("Binance XRP/$ :", BinanXrp_d, "\n")                  # KRW-XRP 조회

    print("Upbit To Biance : 1000만원기준")                      # KRW-XRP 조회
    print("Upbit 1000만원당 XRP :", NoOfXRP)            # KRW-XRP 조회
    print("1000만원당 계약수(10 USD$) :", NoOfCont,"\n")     # KRW-XRP 조회

    print("Biance To Upbit", NoOfContToSnd, "기준")                      # KRW-XRP 조회
    print("Biance To Upbit XRP", NoOfXrpToSnd)                      # KRW-XRP 조회
    print("Upbit 이득(₩)", Revenu)                      # KRW-XRP 조회

    if Kimch_P > KimPMax or Kimch_P < KimPMin :
        post_message(myToken_m,"#coin_ararm","김치프리미엄 :" + str(Kimch_P))

   #s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    #post_message(myToken_m,"#coin","H:" + str(now.tm_hour) + str("Min:") + str(now.tm_min))
    post_message(myToken_m,"#coin","H:" + str(now.tm_hour) + str(" Min:") + str(now.tm_min))
    post_message(myToken_m,"#coin","김치프리미엄 :" + str(Kimch_P))
    post_message(myToken_m,"#coin","UpToBin:" + str(NoOfCont))
    post_message(myToken_m,"#coin","BiToUp("+str(NoOfContToSnd) +str("):") + str(Revenu))

def print_message_s():
    UpbitXrp = get_current_price("KRW-XRP")
    BinanXrp_d = get_binance_xrp()
    BinanXrp_k = BinanXrp_d * currency_rate.convert(1,'USD','KRW')
    NoOfXRP = (10000000/UpbitXrp)*(1-UpbitFee-BinaFee_M) - UpbitTransfFee
    NoOfCont = NoOfXRP * BinanXrp_d / 10
    NoOfXrpToSnd = (NoOfContToSnd * 10 / BinanXrp_d)*(1-BinaFee_T) - BinanTransfFee
    Revenu = NoOfXrpToSnd * UpbitXrp - 10000000
    Kimch_P = UpbitXrp/BinanXrp_k*100-100
    now = time.localtime()

    print("Investing.com cuurent Currency:",currency_rate.convert(1,'USD','KRW'))    # 환율
    print("KimChi P %:", Kimch_P )    # 환율
    print("Upbit XRP :", UpbitXrp)                      # KRW-XRP 조회
    print("Binance XRP/$ :", BinanXrp_d, "\n")                  # KRW-XRP 조회

    print("Upbit 10million ₩ XRP :", NoOfXRP)            # KRW-XRP 조회
    print("contarct per 10million₩(10 USD$) :", NoOfCont,"\n")     # KRW-XRP 조회

    print("Biance To Upbit based on", NoOfContToSnd, "Contract")                      # KRW-XRP 조회
    print("Biance To Upbit XRP", NoOfXrpToSnd)                      # KRW-XRP 조회
    print("Upbit 이득(₩)", Revenu)                      # KRW-XRP 조회


#access = ""          # 본인 값으로 변경
#secret = ""          # 본인 값으로 변경
#upbit = pyupbit.Upbit(access, secret)

schedule.every(1).minutes.do(print_message_m)
schedule.every(5).seconds.do(print_message_s)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)



#print(upbit.get_balance("KRW"))                    # 보유 현금 조회


