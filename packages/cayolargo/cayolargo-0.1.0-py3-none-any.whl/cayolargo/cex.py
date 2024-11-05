# Functions for CEXs (central exchanges) information processing
#   - Binance API
#       get_binance_timeseries()
#       get_binance_multi_timeseries
#       ...


import pandas as pd
from binance.client import Client
from datetime import datetime


def get_binance_timeseries(cpair='BTCUSDT',
                           interval='1d',
                           t_start='2015-01-01',
                           t_end=None,
                           api_key='',
                           api_secret=''):
    """
    Fetches historical time series data for a specified cryptocurrency 
    trading pair from Binance.

    Args:
        cpair (str, optional): The cryptocurrency trading pair to fetch 
                               data for. Default is 'BTCUSDT'.
        interval (str, optional): The time interval for the data. 
                                  Default is '1d' (daily).
                                  Available: 1s, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 
                                             6h, 8h, 12h, 1d, 3d, 1w, 1M (month)
        t_start (str, optional): The starting date for the data in the format 
                                 'YYYY-MM-DD'. Default is '2015-01-01'.
        t_end (str, optional): The ending date for the data in the format 
                               'YYYY-MM-DD'. If not provided, the current date 
                               is used.

    Returns:
        data (DataFrame) : pandas DataFrame or None: A DataFrame containing the historical price 
        and volume data for the specified trading pair, or None if an error occurred.

    Note:
        - This function uses the Binance API to fetch historical price and volume 
          data for a specified trading pair and time interval.
        - To access the Binance API, you need to provide a valid API key and 
          API secret from mycryptokeys.binance_api_key.
        - The data is returned as a DataFrame with the following columns:
          'open_time': The timestamp of the data (UTC) in milliseconds.
          'open': The opening price of the cryptocurrency.
          'high': The highest price during the time interval.
          'low': The lowest price during the time interval.
          'close': The closing price of the cryptocurrency.
          'volume': The trading volume during the time interval.
          'close_time': The timestamp of the closing time (UTC) in milliseconds.
          'qav': Quote asset volume (not used in the function).
          'num_trades': The number of trades during the time interval.
          'taker_base_vol': Taker buy base asset volume (not used in the function).
          'taker_quote_vol': Taker buy quote asset volume (not used in the function).
          'ignore': Ignore (not used in the function).
        - The data is converted to the appropriate data types, and the timestamps are 
          adjusted to the local time zone.
        - If an error occurs during the data retrieval process, the function returns None.
    """

    if api_key == '' or api_secret == '':
        return 'Error: Binance API key or API secret key not provided'

    # client configuration
    client = Client(api_key, api_secret, testnet=False)

    if t_end is None:
        t_end = datetime.now().strftime('%Y-%m-%d')

    try:
        klines = client.get_historical_klines(cpair, interval, t_start, t_end)
        data = pd.DataFrame(klines)
    except:
        data = None  # error fetching data

    if data is not None:
        # create colums name
        cols = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore']

        if data.size > 0:
            data.columns = cols
            data[cols[1:-1]] = data[cols[1:-1]].astype(float)

            # change the timestamp (provided as UTC)
            data.index = [datetime.fromtimestamp(x/1000.0 + 0.001) for x in
                          data.close_time]
            data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')
        else:
            data = None

    return data


def get_binance_multi_timeseries(coin_list,
                                 vs_currency='USDT',
                                 interval='1d',
                                 t_start='2015-01-01',
                                 t_end=None,
                                 api_key='',
                                 api_secret=''):
    """
    Fetches historical time series data for multiple cryptocurrencies against 
    a specified quote currency from Binance.

    Given a list of cryptocurrencies and a quote currency, this function fetches 
    historical price data at a specific time interval from Binance for each 
    cryptocurrency in the list.

    Args:
        coin_list (list): A list of cryptocurrency tickers (symbols) to fetch 
                          data for.
        vs_currency (str, optional): The quote currency against which the 
                                     cryptocurrencies' prices are listed. 
                                     Default is 'USDT'.
        interval (str, optional): The time interval for the data. Default is 
                                  '1d' (daily).
        t_start (str, optional): The starting date for the data in the format 
                                 'YYYY-MM-DD'. Default is '2015-01-01'.
        t_end (str, optional): The ending date for the data in the format 
                               'YYYY-MM-DD'. If not provided, the current date 
                               is used.

    Returns:
        pandas DataFrame: A DataFrame containing the historical price data for 
        each cryptocurrency against the specified quote currency.

    Note:
        - This function calls the 'get_binance_timeseries' function to fetch 
           historical price data for each cryptocurrency in the 'coin_list'.
        - For each cryptocurrency, the 'get_binance_timeseries' function is 
          called with the provided 'vs_currency', 'interval', 't_start', and 't_end'.
        - The resulting data for each cryptocurrency is extracted to create 
          a new DataFrame containing the 'Close' prices, with column names 
          representing each cryptocurrency against the quote currency.
        - If any of the cryptocurrencies' data cannot be fetched or is missing, 
          the corresponding column will contain NaN values in the returned DataFrame.
        - The function prints the progress of data retrieval for each cryptocurrency, 
          indicating if data was successfully fetched ('appended') or skipped if 
          an error occurred ('skipped').
        - The returned DataFrame contains the date-time index and 'Close' prices 
          of each cryptocurrency against the quote currency.
    """
    if api_key == '' or api_secret == '':
        return 'Error in get_binance_multi_timeseries: Binance API key or API secret key not provided'

    df = pd.DataFrame()
    for coin in coin_list:
        cpair = coin + vs_currency
        print(cpair + '... ', end='')
        data = get_binance_timeseries(cpair=cpair,
                                      interval='5m',
                                      t_start=t_start,
                                      t_end=t_end,
                                      api_key=api_key,
                                      api_secret=api_secret)

        if data is not None:
            # extract solely 'Close' prices from 'data' DataFrame
            tmp = pd.DataFrame(data['close'])
            tmp.rename(columns={'close': cpair}, inplace=True)
            if df.size == 0:
                df = tmp.copy()
            else:
                df = pd.merge(left=df, right=tmp,
                              left_index=True, right_index=True)
            print('appended')
        else:
            print('skipped')

    return df


'''
if __name__ == '__main__':

    from mykeys import *

    # test
    df = get_binance_timeseries(cpair='BTCUSDT', 
                                interval='30m', 
                                t_start='2023-08-01', 
                                t_end=None,
                                api_key=binance_api_key, 
                                api_secret=binance_api_secret)
    print(df)
    
    # test
    coin_list = ['BTC', 'XRP', 'SOL', 'ATOM']
    df = get_binance_multi_timeseries(coin_list, 
                                  vs_currency='USDT', 
                                  interval='5m', 
                                  t_start='2023-07-13 14:00', 
                                  t_end='2023-07-14 14:00',
                                  api_key=binance_api_key, 
                                  api_secret=binance_api_secret)
    print(df)
'''
