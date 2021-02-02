#!/usr/bin/python3

import json
import os
import sys

import requests

BULLISH="#20fc03"
LIGHTBULLISH="#63e8ff"
BEARISH="#fc0303"
LIGHTBEARISH="#ff63fa"

CONFIGFILE=os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'config.json')

with open(CONFIGFILE) as configFile:
  CONFIG=json.load(configFile)
  COINS = CONFIG['coins']
  NEWS=CONFIG['newsSites']
  SOCIALS=CONFIG['socials']
  ANALYSIS=CONFIG['analysisTools']

class BinanceAPI:
  BINANCE_API_BASE_URL="https://api.binance.com/api"
  BINANCE_BASE_URL="https://www.binance.com/en"
  BINANCE_WALLET_URL="{}/my/wallet/account/main".format(BINANCE_BASE_URL)
  BINANCE_DASHBOARD_URL="{}/my/dashboard".format(BINANCE_BASE_URL)
  BINANCE_DASHBOARD_URL="{}/my/dashboard".format(BINANCE_BASE_URL)

  BINANCE_TRADING_URL="{}/trade/{}_USDT?layout=basic"


  @staticmethod
  def getMarketInfoFor(coin):
    ticker = requests.get("{}/v3/ticker/24hr?symbol={}".format(BinanceAPI.BINANCE_API_BASE_URL,coin)).json()
    return {
      'price': float(ticker['lastPrice']),
      'percentChange': float(ticker['priceChangePercent'])
    }

  @staticmethod
  def getTradingURL(coin):
    return BinanceAPI.BINANCE_TRADING_URL.format(BinanceAPI.BINANCE_BASE_URL, coin)

  @staticmethod
  def showMenu():
    print("---")
    print("Binance")
    print("--Wallet | href={}".format(BinanceAPI.BINANCE_WALLET_URL))
    print("--Dashboard | href={}".format(BinanceAPI.BINANCE_DASHBOARD_URL))

class CoingeckoAPI:
  COINGECKO_BASE_URL="https://www.coingecko.com/en"

  @staticmethod
  def coinInfo(coinJson):
    return "{}/coins/{}".format(CoingeckoAPI.COINGECKO_BASE_URL,coinJson['coingecko'])

class ArgosAPI:
  @staticmethod
  def separate():
    print('---')

  @staticmethod
  def color(hex):
    color = "color='{}'".format(hex)
    return color

  @staticmethod
  def font(font):
    font = "font='{}'".format(font)
    return font

  @staticmethod
  def refresh(status):
    refresh = 'refresh=' + status
    return refresh

class Cryptos:
  OUTPUT = "<span {} weight='normal'><small><tt>{}:${:.2f}</tt></small></span>"
  @staticmethod
  def camelCaseToPhrase(str): 
    words = [[str[0].upper()]]
    for c in str[1:]: 
        if words[-1][-1].islower() and c.isupper(): 
            words.append(list(c)) 
        else: 
            words[-1].append(c) 
    return (' ').join([''.join(word) for word in words])

  @staticmethod
  def showMenu(menuName,config):
    print(Cryptos.camelCaseToPhrase(menuName))
    for i in config[menuName]:
      print("--{} | href={}".format(i['name'], i['url']))
  
  @staticmethod
  def getCoinMarketInfo(coin):
    marketInfo = BinanceAPI.getMarketInfoFor(coin)
    change = marketInfo['percentChange']
    price = marketInfo['price']
    color=ArgosAPI.color(BULLISH) if change>5 else ArgosAPI.color(LIGHTBULLISH) if change >0 else ArgosAPI.color(BEARISH) if change<-5 else ArgosAPI.color(LIGHTBEARISH)
    return {
      'tradingSymbol': coin,
      'symbol': COINS[coin]['showas'],
      'price': price,
      'color': color,
      'percentChange': change,
      'coingecko': CoingeckoAPI.coinInfo(COINS[coin])
    }

  @staticmethod
  def candlestickPanelURL(coin):
    return "file://{}#coin={}".format(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'cryptoview.html'),coin)

  @staticmethod
  def marketOverview(market):
    print(" - ".join(map(lambda x: Cryptos.OUTPUT.format(x['color'], x['symbol'], x['price']), market)))
  
  @staticmethod
  def showCoinMenu(coin):
    print("{}: ${} (24H: {}%) | {}".format(coin['symbol'], coin['price'], coin['percentChange'], coin['color']))
    print("--Trade | href='{}'".format(BinanceAPI.getTradingURL(coin['symbol'])))
    print("--Candlesticks panel | href='{}'".format(Cryptos.candlestickPanelURL(coin['tradingSymbol'])))
    print("--Coingecko | href='{}'".format(coin['coingecko']))

def __main__():
  market=[]
  for coin in sorted(COINS):
    market.append(Cryptos.getCoinMarketInfo(coin))

  Cryptos.marketOverview(market)
  
  ArgosAPI.separate()
  for m in market:
    Cryptos.showCoinMenu(m)
  
  BinanceAPI.showMenu()
  ArgosAPI.separate()
  Cryptos.showMenu('analysisTools',CONFIG)
  Cryptos.showMenu('socials',CONFIG)
  Cryptos.showMenu('newsSites',CONFIG)
  

__main__()
