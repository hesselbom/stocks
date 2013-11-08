#!/usr/bin/env python

import json
import sys
import pprint
import urllib2

from operator import itemgetter

# Function from http://www.calazan.com/python-function-for-displaying-a-list-of-dictionaries-in-table-format/
def format_as_table(data,
                    keys,
                    header=None,
                    sort_by_key=None,
                    sort_order_reverse=False):
    """Takes a list of dictionaries, formats the data, and returns
    the formatted data as a text table.

    Required Parameters:
        data - Data to process (list of dictionaries). (Type: List)
        keys - List of keys in the dictionary. (Type: List)

    Optional Parameters:
        header - The table header. (Type: List)
        sort_by_key - The key to sort by. (Type: String)
        sort_order_reverse - Default sort order is ascending, if
            True sort order will change to descending. (Type: Boolean)
    """
    # Sort the data if a sort key is specified (default sort order
    # is ascending)
    if sort_by_key:
        data = sorted(data,
                      key=itemgetter(sort_by_key),
                      reverse=sort_order_reverse)

    # If header is not empty, add header to data
    if header:
        # Get the length of each header and create a divider based
        # on that length
        header_divider = []
        for name in header:
            header_divider.append('-' * len(name))

        # Create a list of dictionary from the keys and the header and
        # insert it at the beginning of the list. Do the same for the
        # divider and insert below the header.
        header_divider = dict(zip(keys, header_divider))
        data.insert(0, header_divider)
        header = dict(zip(keys, header))
        data.insert(0, header)

    column_widths = []
    for key in keys:
        column_widths.append(max(len(str(column[key])) for column in data))

    # Create a tuple pair of key and the associated column width for it
    key_width_pair = zip(keys, column_widths)

    format = ('%-*s  ' * len(keys)).strip() + '\n'
    formatted_data = ''
    for element in data:
        data_to_format = []
        # Create a tuple that will be used for the formatting in
        # width, value format
        for pair in key_width_pair:
            data_to_format.append(pair[1])
            data_to_format.append(element[pair[0]])
        formatted_data += format % tuple(data_to_format)
    return formatted_data

# Fetch stock quote
def get_stock_quote(ticker_symbol):
    url = 'http://finance.google.com/finance/info?q=%s' % ticker_symbol
    lines = urllib2.urlopen(url).read().splitlines()
    return json.loads(''.join([x for x in lines if x not in ('// [', ']')]))

if __name__ == '__main__':
    # Fetch tickers from relative 'stocks' file
    data = []
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
    else:
        f = open('stocks')
    lines = [line.strip() for line in f]
    f.close()

    for ticker in lines:
        data.append( get_stock_quote(ticker) )

    header = ['Exchange', 'Ticker', 'Current', 'Change', 'Change %', 'Latest Trade']
    keys = ['e', 't', 'l_cur', 'c', 'cp', 'lt']
    sort_by_key = 't'
    sort_order_reverse = True

    print format_as_table(data, keys, header, sort_by_key, sort_order_reverse)
