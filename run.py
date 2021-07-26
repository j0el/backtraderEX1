import sys
import backtrader as bt
import backtrader.analyzers as btanalyzers
import argparse
from strategies.BuyTheDip import *
from strategies.GoldenCross import *
from strategies.BuyHold import *
from strategies.BollingerBands import *
from strategies.MeanReversion import *
import datetime

# Define start year and ending year for our analysis
FROM_YEAR = 2000
TO_YEAR = 2020

# Adds an argument to bash command 
strategies = {
    "golden_cross": GoldenCross,
    "buy_hold": BuyHold,
    "buy_dip": BuyTheDip,
    "bbands": BollingerBands,
    "mean_reversion": MeanReversion
}

parser = argparse.ArgumentParser()
parser.add_argument("strategy", help="which strategy to run", type=str)
args = parser.parse_args()

if not args.strategy in strategies:
    print("Invalid strategy and/or stock, must be one of {}".format(strategies.keys()))
    sys.exit()

# Argument affects the strategy type
STRATEGY = strategies[args.strategy]
#DATAPATH = './data/{}.csv'.format(STOCK)

# Create a cerebro entity
cerebro = bt.Cerebro()

# Add a strategy
cerebro.addstrategy(STRATEGY)

# Add analyzers
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='myannualreturn')
cerebro.addanalyzer(btanalyzers.Returns, _name='myreturn')
cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')
cerebro.addanalyzer(btanalyzers.Transactions, _name='mytransactions')

# # Add a fixed position size
# cerebro.addsizer(bt.sizers.FixedSize, stake=100)

# Create a Data Feed
stock_set = {
    'SPY', 'QQQ', 'DIA', 'AAPL', 'XLV',
    'BAC', 'DE', 'EWZ', 'FXE', 'IBB',
    'IWM', 'SLV', 'GLD', 'T', 'TSLA',
    'WFC', 'FSLR', 'IBM', 'MSFT', 'V',
    'NFLX', 'PYPL', 'COF', 'EEM', 'AMZN',
    'EWW', 'FXI', 'RSX', 'TLT', 'TBT'
    'XLF', 'VXX', 'CCL', 'M', 'JNK',
    'NKE', 'BBY', 'GPS', 'TGT', 'WMT',
    'BABA', 'LOW', 'X', 'BA', 'RACE',
    'CPB', 'K', 'KO', 'HD', 'JD',
    'KR', 'MGM', 'JNJ', 'MS', 'CAH',
    'VZ', 'AAL', 'JPM', 'TWTR', 'F',
    'C', 'LVS', 'COP', 'CVX', 'CVS'}

for stock in stock_set:

    data = bt.feeds.YahooFinanceCSVData(
        dataname='./data/{}.csv'.format(stock),
        # Do not pass values before this date
        fromdate=datetime.datetime(FROM_YEAR, 1, 1),
        # Do not pass values before this date
        todate=datetime.datetime(TO_YEAR, 12, 31),
        # Do not pass values after this date
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data, name=stock)

# Set our desired cash start
cerebro.broker.setcash(10000.0)

# Print out results
print("\n*** Results ***")
beginning_cash = cerebro.broker.getvalue()
print('Starting Portfolio Value: %.3f' % cerebro.broker.getvalue())

# Run everything
backtest = cerebro.run()
backtest = backtest[0]

# Final Results
print('Final Portfolio Value: %.3f' % cerebro.broker.getvalue())
ending_cash = cerebro.broker.getvalue()
print(f"Total profit: %.3f" % (ending_cash - beginning_cash))

# Analysis
print("\n*** Analysis ***")
print("Sharpe Ratio: %.3f" % backtest.analyzers.mysharpe.get_analysis()['sharperatio'])
print("Mean annual return (pct): %.2f" % backtest.analyzers.myreturn.get_analysis()['rnorm100'], "&")
print("Max drawdown (pct): %.2f" % backtest.analyzers.mydrawdown.get_analysis()['max']['drawdown'], "%")
print("Max drawdown ($): %.0f" % backtest.analyzers.mydrawdown.get_analysis()['max']['moneydown'])
print("Max drawdown length (days): %.0f" % backtest.analyzers.mydrawdown.get_analysis()['max']['len'])

print("\n")

transactions = False

if transactions:
    print("*** Transaction breakdown ***")
    for key in backtest.analyzers.mytransactions.get_analysis().keys():
        print("Date:", key.date(), "| Symbol:", backtest.analyzers.mytransactions.get_analysis()[key][0][3], "| Price:%.2f" % backtest.analyzers.mytransactions.get_analysis()[key][0][1], "| Type:", ["Buy" if  x < 0 else "Sell" for x in [backtest.analyzers.mytransactions.get_analysis()[key][0][4]]][0], "| N_Shares:", backtest.analyzers.mytransactions.get_analysis()[key][0][0])
else:
    print("Transactions not printed")

#cerebro.plot()