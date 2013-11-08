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

Automatic updates / Watch
=====
You can make it autoupdate your list by appending how many seconds it should wait before updating. Like this:
```
./stocks.py stocks.txt 5
```
That will try to update every 5 sec.

If the request for stocks take longer than the 5 seconds it will only check for new stocks once the current request has been returned.
