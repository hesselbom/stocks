stocks
======

Commandline stock update.

Reads file from first argument.

Installation
============
First set as executable:
```
chmod +x stocks.py
```

Then create a stocks file:
```
nano stocks.txt
```

And enter any tickers in this format:
```
TWTR
STO:RATO-B
```
Now you can run the following to get an update on all tickers:
```
./stocks.py stocks.txt
```
