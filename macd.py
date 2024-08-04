import numpy as np
import ta
import json
import pandas as pd
import ta.momentum
import ta.trend

import yfinance as yf

import matplotlib.pyplot as plt

interval = "1h"
# interval = "30m"


df = yf.download("BTC-USD", start="2022-09-01", interval=interval)


def MACD(df):
    df["EMA12"] = df.Close.ewm(span=12).mean()
    df["EMA26"] = df.Close.ewm(span=26).mean()

    df["MACD"] = df.EMA12 - df.EMA26
    df["signal"] = df.MACD.ewm(span=9).mean()


MACD(df)


# plt.plot(df.signal, label="signal", color="red")
# plt.plot(df.MACD, label="MACD", color="green")
# plt.legend()
# plt.show()


Buy, Sell = [], []

for i in range(2, len(df)):
    if (
        df.MACD.iloc[i] > df.signal.iloc[i]
        and df.MACD.iloc[i - 1] < df.signal.iloc[i - 1]
    ):
        Buy.append(i)
    elif (
        df.MACD.iloc[i] < df.signal.iloc[i]
        and df.MACD.iloc[i - 1] > df.signal.iloc[i - 1]
    ):
        Sell.append(i)

# print(Buy, Sell)

plt.scatter(df.iloc[Buy].index, df.iloc[Buy].Close, color="green", label="Buy")
plt.scatter(df.iloc[Sell].index, df.iloc[Sell].Close, color="red", label="Sell")
plt.plot(df.Close, color="k", label="Close")
plt.legend()
plt.show()


RealBuys = [i + 1 for i in Buy]
RealSells = [i + 1 for i in Sell]

Buyprices = df.Open.iloc[RealBuys]
Sellprices = df.Open.iloc[RealSells]

if Sellprices.index[0] < Buyprices.index[0]:
    Sellprices = Sellprices.drop(Sellprices.index[0])
elif Buyprices.index[-1] > Sellprices.index[-1]:
    Buyprices = Buyprices.drop(Buyprices.index[-1])


profitsrel = []
for i in range(len(Sellprices)):
    profitsrel.append((Sellprices[i] - Buyprices[i]) / Buyprices[i])


print(sum(profitsrel) / len(profitsrel))
