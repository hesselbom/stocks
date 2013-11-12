#!/usr/bin/env python

import json
import sys
import pprint
import urllib2
import os

from time import time, sleep, strftime
from operator import itemgetter
from tabulate import tabulate

# Fetch stock quote
def get_stock_quote(ticker_symbol):
    url = 'http://finance.google.com/finance/info?q=%s' % ticker_symbol
    lines = urllib2.urlopen(url).read().splitlines()
    return json.loads(''.join([x for x in lines if x not in ('// [', ']')]))

def format_quote(ticker):
    ticker['c'] = format_number(ticker['c'])
    ticker['cp'] = format_number(ticker['cp'])
    return ticker

def format_number(number):
    if float(number) > 0:
        return '\033[92m' + number + '\033[0m'
    elif float(number) < 0:
        return '\033[31m' + number + '\033[0m'
    else:
        return '\033[31m' + number + '\033[0m'

def update(lines):
    data = []

    header = ['Exchange', 'Ticker', 'Current', 'Change', 'Change %', 'Latest Trade']
    keys = ['e', 't', 'l', 'c', 'cp', 'lt']
    sort_by_key = 't'
    sort_order_reverse = True

    x = [[]]

    for ticker in lines:
        quote = format_quote(get_stock_quote(ticker))
        data.append( [quote['e'], quote['t'], quote['l'], quote['c'], quote['cp'], quote['lt']] )

    return '\033[1;31mUpdated at: %s\033[0m\n%s' % (strftime("%H:%M:%S"), tabulate(data, header, tablefmt="orgtbl"))

if __name__ == '__main__':
    # Fetch tickers from relative 'stocks' file
    watch = 0.0
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        if len(sys.argv) > 2:
            watch = int(sys.argv[2])
    else:
        f = open('stocks')
    lines = [line.strip() for line in f]
    f.close()

    try:
        if watch <= 0:
            print update(lines)
        else:
            startTime = time()
            output = update(lines)
            os.system('cls' if os.name=='nt' else 'clear')
            print output
            endTime = time() - startTime
            sleep(max(0, watch-endTime))

            while True:
                startTime = time()
                output = update(lines)
                os.system('cls' if os.name=='nt' else 'clear')
                print output
                endTime = time() - startTime
                sleep(max(0, watch-endTime))
    except KeyboardInterrupt:
        print '\033[33mGoodbye!\033[0m\n'
        sys.exit(0)
