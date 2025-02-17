"""
Data should contain headers: Date | Open | High | Low | Close | Adj Close | Volume
"""
import requests
import pandas as pd
import time

def get_price_data(api_key, stock):
    """
    Makes an Alpha Vantage API call.
    Returns json with open, high, low, close information of specified stock.
    """
    api_key = api_key
    stock = stock
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock}&outputsize=full&apikey={api_key}"
    data = requests.get(url).json()

    return data

def create_dataframe(data):
    """
    Puts the price data into a dataframe and cleans it
    """
    # Put data into dataframe
    dataframe = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

    for key in data["Time Series (Daily)"].keys():
        dataframe = dataframe.append(
            pd.Series(
                [key,
                data["Time Series (Daily)"][key]["1. open"],
                data["Time Series (Daily)"][key]["2. high"],
                data["Time Series (Daily)"][key]["3. low"],
                data["Time Series (Daily)"][key]["4. close"],
                data["Time Series (Daily)"][key]["5. adjusted close"],
                data["Time Series (Daily)"][key]["6. volume"]], index=dataframe.columns
            ), ignore_index=True
        )

    # Clean up dataframe
    dataframe.sort_values("Date", ascending=True, inplace=True, ignore_index=True)

    return dataframe

def save_csv(dataframe, stock):
    """
    Saves dataframe as CSV in current directory
    """
    dataframe.to_csv(f"./data/{stock}.csv", index=False)

if __name__ == '__main__':

    start = time.time()

    api_key = 'VHOI1ERJ34C0FKHZ'

    stock_list = [
        'AAL', 'AAPL', 'AMD', 'AMZN', 'BA',
        'BABA', 'BAC', 'BBY', 'BIDU', 'BLK',
        'BOX', 'BX', 'C', 'CAH', 'CCL',
        'CLX', 'COF', 'COP', 'COST', 'CPB',
        'CRM', 'CVS', 'CVX', 'CZR', 'DAL',
        'DE', 'DECK', 'DIA', 'DVN', 'EEM',
        'EWW', 'EWZ', 'F', 'FB', 'FSLR',
        'FXE', 'FXI', 'GE', 'GLD', 'GOOG',
        'GPRO', 'GPS', 'HD', 'IBB',
        'IBM', 'IBND', 'IWM', 'JD', 'JNJ',
        'JNK', 'JPM', 'K', 'KHC', 'KO',
        'KR', 'LOW', 'LVS', 'M', 'MGM',
        'MS', 'MSFT', 'MU', 'NFLX', 'NKE',
        'PFE', 'PYPL', 'QQQ', 'RACE', 'RSX',
        'SLV', 'SPY', 'STMP', 'T', 'TBT',
        'TGT', 'TLT', 'TSLA', 'TWTR', 'USO',
        'V', 'VB', 'VXX', 'VZ', 'WFC',
        'WMT', 'X', 'XLF',
        'XLV', 'YELP'
        ]

    for stock in stock_list:

        data = get_price_data(api_key, stock)
        
        dataframe = create_dataframe(data)

        save_csv(dataframe, stock)

        time.sleep(5) # To avoid the program from stopping

    end = time.time()

    run_time = end - start

    print("\nProgram run time: %.2f" % run_time, "seconds\n")
        
    ### API call on RUT not working ###
    # data = get_price_data(api_key, 'RUT')
    # print(data)

