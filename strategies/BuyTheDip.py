"""
Simple Buy-The-Dip strategy: If stock is down for 3 consecutive days, then buy
Sell after desired number of days.
"""

import backtrader as bt

STOCK = 'SPY'
N_DAYS_HOLD = 5

class BuyTheDip(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED {}".format(order.executed.price))
            elif order.issell():
                self.log("SELL EXECUTED {}".format(order.executed.price))

            self.bar_executed = len(self)

        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    if self.dataclose[-2] < self.dataclose[-3]:

                        # BUY, BUY, BUY!!! (with all possible default parameters)
                        self.log('BUY CREATE, %.2f' % self.dataclose[0])
                        self.order = self.buy()

        else:
            if len(self) >= (self.bar_executed + N_DAYS_HOLD):
                self.log("SELL CREATED {}".format(self.dataclose[0]))
                self.order = self.sell()