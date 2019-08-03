import FrameWork.debug as debug
from sqlite3 import Error
import os
import app.db as db
import FrameWork.debug as debug
import vars
import app.MiddleWare as mw
from poloniex import Poloniex
import requests


strFooterPath=os.path.dirname(__file__) + vars._FooterFile

def LendingRates():
    print("Showing LendingRates polled from poloniex")

    retVal=getLendingData()

    strPath=os.path.dirname(__file__).replace("app","")  + vars._PolLend
    return mw.getTemplate(strPath).replace("%LOWEST_LEND%", str(retVal))

def getLendingData():
    url = 'https://poloniex.com/public?'
    r = requests.post(url, dict(
            command='returnLoanOrders',
            currency='BTC'))
    print(r.headers)
    print(r.text) # or r.json()
    return r.headers
