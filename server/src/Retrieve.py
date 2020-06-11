"""
11-06-2020 crisb0
---------------------------
Get financial data from Yahoo finance
"""
from datetime import datetime, timedelta
from calendar import monthrange
import common.ConfigParser as cfg

from threading import Thread
import sys
from queue import Queue
import csv
import urllib3
import requests

from server.err.YahooAPI import *

MAX_THREADS = 5



class YahooAPI:
    def __init__(self):
        self.htmlUrl = cfg.parse('yahoo', key='htmlUrl')
        self.csvUrl = cfg.parse('yahoo', key='csvUrl')
        self.q = Queue(MAX_THREADS)

    """
    https://au.finance.yahoo.com/quote/^CMC200/history?period1=1591833600&period2=1591833600&interval=1d&filter=history&frequency=1d
    """
    def generatehtmlURL(self, tickers, start, end):
        for t in tickers: 
            args = [self.htmlUrl, \
            'quote/', t, 
            '/history?period1=', str(int(start.timestamp())), 
            '&period2=', str(int(end.timestamp())), 
            '&interval=', '1d', 
            '&filter=history', 
            '&frequency=', '1d']
            yield ''.join(args)
    
    """
    https://query1.finance.yahoo.com/v7/finance/download/^CMC200?period1=1591883000&period2=1591969400&interval=1d&events=history
    """
    def generateCsvURL(self, tickers, start, end):
        for t in tickers: 
            args = [self.csvUrl,
            'v7/finance/download/', t, 
            '?period1=', str(int(start.timestamp())), 
            '&period2=', str(int(end.timestamp())), 
            '&interval=', '1d', 
            '&events=history']
            yield ''.join(args)
    """
    param: tickers=set() start=date period=[1d, 1w, 1m, 6m, 1y, 5y, MAX]
    """

    def get(self, tickers, start, period=None):
        if not start:
            start = datetime.now()
        end = self._getEndDate(start, period=period)

        for i in range(MAX_THREADS):
            t = Thread(target=self._getWorker)
            t.daemon = True; t.start()
        
        try: 
            for url in self.generateCsvURL(tickers, start, end):
                self.q.put(url.strip())
            self.q.join()
        except:
            raise ThreadError("Unable to get all requests")

    def _getWorker(self):
        s = requests.Session()
        while True:
            url = self.q.get()
            response = s.get(url)
            res = csv.reader(response.content.decode('utf-8').splitlines())
            for r in res:
                print(r)
            self.q.task_done()

    def _getEndDate(self, start, **kw):
        period = kw.get('period')
        if not period: 
            period = '1d'
        return start + timedelta(days=int(period[:-1])*self._getDays(period[-1]))

    def _getDays(self,period):
        today = datetime.now()
        if period == 'w':
            return 7
        elif period == 'm':
            return monthrange(today.year, today.month)[1]
        elif period == 'y':
            return 365
        return 1

if __name__ == "__main__":
    new = YahooAPI()
    new.get(['^CMC200', 'AUDUSD=X', 'CL=F', '^AORD'], datetime.now())

