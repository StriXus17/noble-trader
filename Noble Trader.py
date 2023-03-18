import ccxt
import pandas as pd
import pandas_ta as ta
import sys
import requests
import time
from playground import check_crossing
binance_api = "https://api.binance.com/api/v3/exchangeInfo"
kucoin_api = "https://api.kucoin.com/api/v1/symbols"
response = requests.get(binance_api)
response_k = requests.get(kucoin_api)
if response_k.status_code == 200:
    data = response_k.json()
    symbols_k = [symbolk["symbol"] for symbolk in data["data"]]
if response.status_code == 200:
    data = response.json()
    symbols = [symbol["symbol"] for symbol in data["symbols"]]
crossed = {}
hold = {}
symbols = set(symbols + symbols_k)
symbols = list(filter(lambda x:"USDT" in x or "BTC" in x or "ETH" in x,symbols))
print(len(symbols))
TOKEN = "6118801193:AAHwaXafeBG2kkxL7OqQHxs8q4qzPqPr0Yg"
chat_id = "-1001714433847"
while True:
    valid = []
    for x in symbols:
        try:
            if x not in crossed:
                crossed[x] = None
            try:
                rsi,sma = check_crossing(x)
            except:
                continue
            k = crossed[x]
            if(rsi > sma + 3):
                k = True
            elif(sma > rsi + 1):
                k = False
            if crossed[x] !=  k:
                if crossed[x] == False:
                    message = f" هناك تقاطع إيجابي في عملة {x} ✅"
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                    r = requests.get(url)
                    print("New:",x,crossed[x],rsi,sma,"Old:",tmp[0],tmp[1])
                crossed[x] = k
            tmp = [rsi,sma]
            valid.append(x)
            print("Coins Checked:",len(valid),"/",len(symbols),"\t\t",end="\r",flush=True)
        except:
            continue
print("Refreshing in 5 Mins")
time.sleep(300)
