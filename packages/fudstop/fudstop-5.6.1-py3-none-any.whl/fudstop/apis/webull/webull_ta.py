import re
import pandas as pd
import asyncio
import time
import ta.momentum
import ta.others
import ta.trend
import ta.volatility
import ta.volume

import httpx
import numpy as np
import ta
class WebullTA:
    def __init__(self):
        self.ticker_df = pd.read_csv('files/ticker_csv.csv')
        self.ticker_to_id_map = dict(zip(self.ticker_df['ticker'], self.ticker_df['id']))
        self.intervals_to_scan = ['m5', 'm30', 'm60', 'm120', 'm240', 'd', 'w', 'm']  # Add or remove intervals as needed
    def parse_interval(self,interval_str):
        pattern = r'([a-zA-Z]+)(\d+)'
        match = re.match(pattern, interval_str)
        if match:
            unit = match.group(1)
            value = int(match.group(2))
            if unit == 'm':
                return value * 60
            elif unit == 'h':
                return value * 3600
            elif unit == 'd':
                return value * 86400
            else:
                raise ValueError(f"Unknown interval unit: {unit}")
        else:
            raise ValueError(f"Invalid interval format: {interval_str}")
    async def get_webull_id(self, symbol):
        """Converts ticker name to ticker ID to be passed to other API endpoints from Webull."""
        ticker_id = self.ticker_to_id_map.get(symbol)
        return ticker_id

    async def get_candle_data(self, ticker, interval, headers, count:str='800'):
        try:
            timeStamp = None
            if ticker == 'I:SPX':
                ticker = 'SPX'
            elif ticker =='I:NDX':
                ticker = 'NDX'
            elif ticker =='I:VIX':
                ticker = 'VIX'
            elif ticker == 'I:RUT':
                ticker = 'RUT'
            elif ticker == 'I:XSP':
                ticker = 'XSP'
            



            if timeStamp is None:
                # if not set, default to current time
                timeStamp = int(time.time())
            tickerid = await self.get_webull_id(ticker)
            base_fintech_gw_url = f'https://quotes-gw.webullfintech.com/api/quote/charts/query-mini?tickerId={tickerid}&type={interval}&count={count}&timestamp={timeStamp}&restorationType=1&extendTrading=1'

            interval_mapping = {
                'm5': '5 min',
                'm30': '30 min',
                'm60': '1 hour',
                'm120': '2 hour',
                'm240': '4 hour',
                'd': 'day',
                'w': 'week',
                'm': 'month'
            }

            timespan = interval_mapping.get(interval)

            async with httpx.AsyncClient(headers=headers) as client:
                data = await client.get(base_fintech_gw_url)
                r = data.json()
                if r and isinstance(r, list) and 'data' in r[0]:
                    data = r[0]['data']

     
                    split_data = [row.split(",") for row in data]
                    print(split_data)
                    df = pd.DataFrame(split_data, columns=['Timestamp', 'Open', 'Close', 'High', 'Low', 'Vwap', 'Volume', 'Avg'])
                    df['Timestamp'] = pd.to_numeric(df['Timestamp'], errors='coerce')
                    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', utc=True)

                    # First localize to UTC, then convert to 'US/Eastern' and remove timezone info
                    df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern').dt.tz_localize(None)
                    df['Ticker'] = ticker
                    df['timespan'] = interval


                    return df[::-1]
                
        except Exception as e:
            print(e)


    # Simulating async TA data fetching for each timeframe
    async def fetch_ta_data(self, timeframe, data):
        # Simulate an async operation to fetch data (e.g., from an API)

        return data.get(timeframe, {})
    async def async_scan_candlestick_patterns(self, df, interval):
        """
        Asynchronously scans for candlestick patterns in the given DataFrame over the specified interval.

        Parameters:
        - df (pd.DataFrame): DataFrame containing market data with columns ['High', 'Low', 'Open', 'Close', 'Volume', 'Vwap', 'Timestamp']
        - interval (str): Resampling interval based on custom mappings (e.g., 'm5', 'm30', 'd', 'w', 'm')

        Returns:
        - pd.DataFrame: DataFrame with additional columns indicating detected candlestick patterns and their bullish/bearish nature
        """
        # Mapping custom interval formats to Pandas frequency strings
        interval_mapping = {
            'm5': '5min',
            'm30': '30min',
            'm60': '60min',  # or '1H'
            'm120': '120min',  # or '2H'
            'm240': '240min',  # or '4H'
            'd': '1D',
            'w': '1W',
            'm': '1M'
            # Add more mappings as needed
        }

        # Convert the interval to Pandas frequency string
        pandas_interval = interval_mapping.get(interval)
        if pandas_interval is None:
            raise ValueError(f"Invalid interval '{interval}'. Please use one of the following: {list(interval_mapping.keys())}")

        # Ensure 'Timestamp' is datetime and set it as the index
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)

        # Since data is most recent first, sort in ascending order for resampling
        df.sort_index(ascending=True, inplace=True)

        # Asynchronous resampling (using run_in_executor to avoid blocking the event loop)
        loop = asyncio.get_event_loop()
        ohlcv = await loop.run_in_executor(None, self.resample_ohlcv, df, pandas_interval)

        # Asynchronous pattern detection
        patterns_df = await loop.run_in_executor(None, self.detect_patterns, ohlcv)

        # Since we want the most recent data first, reverse the DataFrame
        patterns_df = patterns_df.iloc[::-1].reset_index()

        return patterns_df

    def resample_ohlcv(self, df, pandas_interval):
        ohlcv = df.resample(pandas_interval).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
            'Vwap': 'mean'
        }).dropna()
        return ohlcv

    async def async_scan_candlestick_patterns(self, df, interval):
        """
        Asynchronously scans for candlestick patterns in the given DataFrame over the specified interval.
        """
        # Mapping custom interval formats to Pandas frequency strings
        interval_mapping = {
            'm5': '5min',
            'm30': '30min',
            'm60': '60min',  # or '1H'
            'm120': '120min',  # or '2H'
            'm240': '240min',  # or '4H'
            'd': '1D',
            'w': '1W',
            'm': '1M'
        }

        # Convert the interval to Pandas frequency string
        pandas_interval = interval_mapping.get(interval)
        if pandas_interval is None:
            raise ValueError(f"Invalid interval '{interval}'. Please use one of the following: {list(interval_mapping.keys())}")

        # Ensure 'Timestamp' is datetime and set it as the index
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)

        # Since data is most recent first, sort in ascending order for resampling
        df.sort_index(ascending=True, inplace=True)

        # Asynchronous resampling (using run_in_executor to avoid blocking the event loop)
        loop = asyncio.get_event_loop()
        ohlcv = await loop.run_in_executor(None, self.resample_ohlcv, df, pandas_interval)

        # Asynchronous pattern detection
        patterns_df = await loop.run_in_executor(None, self.detect_patterns, ohlcv)

        # No need to reverse the DataFrame; keep it in ascending order
        # patterns_df = patterns_df.iloc[::-1].reset_index()

        return patterns_df.reset_index()
   
    def resample_ohlcv(self, df, pandas_interval):
        ohlcv = df.resample(pandas_interval).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
            'Vwap': 'mean'
        }).dropna()
        return ohlcv
    def detect_patterns(self, ohlcv):
        # Initialize pattern columns
        patterns = ['hammer', 'inverted_hammer', 'hanging_man', 'shooting_star', 'doji',
                    'bullish_engulfing', 'bearish_engulfing', 'bullish_harami', 'bearish_harami',
                    'morning_star', 'evening_star', 'piercing_line', 'dark_cloud_cover',
                    'three_white_soldiers', 'three_black_crows', 'abandoned_baby',
                    'rising_three_methods', 'falling_three_methods', 'three_inside_up', 'three_inside_down',
                     'gravestone_doji', 'butterfly_doji', 'harami_cross', 'tweezer_top', 'tweezer_bottom']



        for pattern in patterns:
            ohlcv[pattern] = False

        ohlcv['signal'] = None  # To indicate Bullish or Bearish signal

        # Iterate over the DataFrame to detect patterns
        for i in range(len(ohlcv)):
            curr_row = ohlcv.iloc[i]
            prev_row = ohlcv.iloc[i - 1] if i >= 1 else None
            prev_prev_row = ohlcv.iloc[i - 2] if i >= 2 else None



            uptrend = self.is_uptrend(ohlcv, i)
            downtrend = self.is_downtrend(ohlcv, i)


            # Single-candle patterns
            if downtrend and self.is_hammer(curr_row):
                ohlcv.at[ohlcv.index[i], 'hammer'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
            if downtrend and self.is_inverted_hammer(curr_row):
                ohlcv.at[ohlcv.index[i], 'inverted_hammer'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
            if uptrend and self.is_hanging_man(curr_row):
                ohlcv.at[ohlcv.index[i], 'hanging_man'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
            if uptrend and self.is_shooting_star(curr_row):
                ohlcv.at[ohlcv.index[i], 'shooting_star'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
            if downtrend and self.is_dragonfly_doji(curr_row):
                ohlcv.at[ohlcv.index[i], 'dragonfly_doji'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
            if uptrend and self.is_gravestone_doji(curr_row):
                ohlcv.at[ohlcv.index[i], 'gravestone_doji'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'

            # Two-candle patterns
            if prev_row is not None:
                if downtrend and self.is_bullish_engulfing(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bullish_engulfing'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_bearish_engulfing(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bearish_engulfing'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_bullish_harami(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bullish_harami'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_bearish_harami(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bearish_harami'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_piercing_line(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'piercing_line'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_dark_cloud_cover(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'dark_cloud_cover'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_tweezer_bottom(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'tweezer_bottom'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_tweezer_top(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'tweezer_top'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_harami_cross(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'harami_cross'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'neutral'

            # Three-candle patterns
            if prev_row is not None and prev_prev_row is not None:
                if downtrend and self.is_morning_star(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'morning_star'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_evening_star(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'evening_star'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_three_white_soldiers(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_white_soldiers'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_three_black_crows(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_black_crows'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_three_inside_up(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_inside_up'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_three_inside_down(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_inside_down'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if self.is_abandoned_baby(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'abandoned_baby'] = True
                    if curr_row['Close'] > prev_row['Close']:
                        ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                    else:
                        ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_rising_three_methods(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'rising_three_methods'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_falling_three_methods(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'falling_three_methods'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'

        return ohlcv
    def is_gravestone_doji(self, row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Close'], row['Open'])
        lower_shadow = min(row['Close'], row['Open']) - row['Low']
        return total_range != 0 and body_length <= 0.1 * total_range and lower_shadow == 0 and upper_shadow > 2 * body_length
        
    def is_three_inside_up(self, prev_prev_row, prev_row, curr_row):
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        second_bullish = prev_row['Close'] > prev_row['Open']
        third_bullish = curr_row['Close'] > curr_row['Open']
        return (first_bearish and second_bullish and third_bullish and
                prev_row['Open'] > prev_prev_row['Close'] and prev_row['Close'] < prev_prev_row['Open'] and
                curr_row['Close'] > prev_prev_row['Open'])


    def is_tweezer_top(self, prev_row, curr_row):
        return (prev_row['High'] == curr_row['High']) and (prev_row['Close'] > prev_row['Open']) and (curr_row['Close'] < curr_row['Open'])

    def is_tweezer_bottom(self, prev_row, curr_row):
        return (prev_row['Low'] == curr_row['Low']) and (prev_row['Close'] < prev_row['Open']) and (curr_row['Close'] > curr_row['Open'])

    def is_dragonfly_doji(self, row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Close'], row['Open'])
        lower_shadow = min(row['Close'], row['Open']) - row['Low']
        return total_range != 0 and body_length <= 0.1 * total_range and upper_shadow == 0 and lower_shadow > 2 * body_length


    def is_uptrend(self, df: pd.DataFrame, length: int =7) -> bool:
        """
        Check if the dataframe shows an uptrend over the specified length.
        
        An uptrend is defined as consecutive increasing 'Close' values for the given length.
        The dataframe is assumed to have the most recent candle at index 0.
        """
        try:
            if len(df) < length:
                raise ValueError(f"DataFrame length ({len(df)}) is less than the specified length ({length})")
            
            # Since the most recent data is at index 0, we need to reverse the direction of comparison.
            return (df['Close'].iloc[:length].diff(periods=-1).iloc[:-1] > 0).all()

        except Exception as e:
            print(f"Failed - {e}")

    def is_downtrend(self, df: pd.DataFrame, length: int = 7) -> bool:
        """
        Check if the dataframe shows a downtrend over the specified length.
        
        A downtrend is defined as consecutive decreasing 'Close' values for the given length.
        """
        try:
            if len(df) < length:
                raise ValueError(f"DataFrame length ({len(df)}) is less than the specified length ({length})")
            
            # Since the most recent data is at index 0, we need to reverse the direction of comparison.
            return (df['Close'].iloc[:length].diff(periods=-1).iloc[:-1] < 0).all()
        except Exception as e:
            print(f"Failed - {e}")

    def is_hammer(self,row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Close'], row['Open'])
        lower_shadow = min(row['Close'], row['Open']) - row['Low']
        return (lower_shadow >= 2 * body_length) and (upper_shadow <= body_length)

    def is_inverted_hammer(self,row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Open'], row['Close'])
        lower_shadow = min(row['Open'], row['Close']) - row['Low']
        return (upper_shadow >= 2 * body_length) and (lower_shadow <= body_length)

    def is_hanging_man(self, row):
        return self.is_hammer(row)

    def is_shooting_star(self, row):
        return self.is_inverted_hammer(row)

    def is_doji(self,row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        return total_range != 0 and body_length <= 0.1 * total_range

    def is_bullish_engulfing(self,prev_row, curr_row):
        return (prev_row['Close'] < prev_row['Open']) and (curr_row['Close'] > curr_row['Open']) and \
            (curr_row['Open'] < prev_row['Close']) and (curr_row['Close'] > prev_row['Open'])

    def is_bearish_engulfing(self,prev_row, curr_row):
        return (prev_row['Close'] > prev_row['Open']) and (curr_row['Close'] < curr_row['Open']) and \
            (curr_row['Open'] > prev_row['Close']) and (curr_row['Close'] < prev_row['Open'])

    def is_bullish_harami(self,prev_row, curr_row):
        return (prev_row['Open'] > prev_row['Close']) and (curr_row['Open'] < curr_row['Close']) and \
            (curr_row['Open'] > prev_row['Close']) and (curr_row['Close'] < prev_row['Open'])

    def is_bearish_harami(self,prev_row, curr_row):
        return (prev_row['Open'] < prev_row['Close']) and (curr_row['Open'] > curr_row['Close']) and \
            (curr_row['Open'] < prev_row['Close']) and (curr_row['Close'] > prev_row['Open'])

    def is_morning_star(self,prev_prev_row, prev_row, curr_row):
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        second_small_body = abs(prev_row['Close'] - prev_row['Open']) < abs(prev_prev_row['Close'] - prev_prev_row['Open']) * 0.3
        third_bullish = curr_row['Close'] > curr_row['Open']
        first_midpoint = (prev_prev_row['Open'] + prev_prev_row['Close']) / 2
        third_close_above_first_mid = curr_row['Close'] > first_midpoint
        return first_bearish and second_small_body and third_bullish and third_close_above_first_mid

    def is_evening_star(self,prev_prev_row, prev_row, curr_row):
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        second_small_body = abs(prev_row['Close'] - prev_row['Open']) < abs(prev_prev_row['Close'] - prev_prev_row['Open']) * 0.3
        third_bearish = curr_row['Close'] < curr_row['Open']
        first_midpoint = (prev_prev_row['Open'] + prev_prev_row['Close']) / 2
        third_close_below_first_mid = curr_row['Close'] < first_midpoint
        return first_bullish and second_small_body and third_bearish and third_close_below_first_mid

    def is_piercing_line(self,prev_row, curr_row):
        first_bearish = prev_row['Close'] < prev_row['Open']
        second_bullish = curr_row['Close'] > curr_row['Open']
        open_below_prev_low = curr_row['Open'] < prev_row['Low']
        prev_midpoint = (prev_row['Open'] + prev_row['Close']) / 2
        close_above_prev_mid = curr_row['Close'] > prev_midpoint
        return first_bearish and second_bullish and open_below_prev_low and close_above_prev_mid
        
    def has_gap_last_4_candles(self, ohlcv, index):
        """
        Checks if there's a gap within the last 4 candles, either up or down.
        A gap up occurs when the current open is higher than the previous close,
        and a gap down occurs when the current open is lower than the previous close.
        
        :param ohlcv: The OHLCV dataframe with historical data.
        :param index: The current index in the dataframe.
        :return: Boolean value indicating whether a gap exists in the last 4 candles.
        """
        # Ensure there are at least 4 candles to check
        if index < 3:
            return False

        # Iterate through the last 4 candles
        for i in range(index - 3, index):
            curr_open = ohlcv.iloc[i + 1]['Open']
            prev_close = ohlcv.iloc[i]['Close']
            
            # Check for a gap (either up or down)
            if curr_open > prev_close or curr_open < prev_close:
                return True  # A gap is found

        return False  # No gap found in the last 4 candles

    def is_abandoned_baby(self, prev_prev_row, prev_row, curr_row):
        # Bullish Abandoned Baby
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        doji = self.is_doji(prev_row)
        third_bullish = curr_row['Close'] > curr_row['Open']
        
        # Check for gaps
        gap_down = prev_row['Open'] < prev_prev_row['Close'] and prev_row['Close'] < prev_prev_row['Low']
        gap_up = curr_row['Open'] > prev_row['Close'] and curr_row['Close'] > prev_row['High']
        
        return first_bearish and doji and third_bullish and gap_down and gap_up

    def is_harami_cross(self, prev_row, curr_row):
        # Harami Cross is a special form of Harami with the second candle being a Doji
        return self.is_bullish_harami(prev_row, curr_row) and self.is_doji(curr_row)

    def is_rising_three_methods(self, prev_prev_row, prev_row, curr_row):
        # Rising Three Methods (Bullish Continuation)
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        small_bearish = prev_row['Close'] < prev_row['Open'] and prev_row['Close'] > prev_prev_row['Open']
        final_bullish = curr_row['Close'] > curr_row['Open'] and curr_row['Close'] > prev_prev_row['Close']
        
        return first_bullish and small_bearish and final_bullish

    def is_falling_three_methods(self, prev_prev_row, prev_row, curr_row):
        # Falling Three Methods (Bearish Continuation)
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        small_bullish = prev_row['Close'] > prev_row['Open'] and prev_row['Close'] < prev_prev_row['Open']
        final_bearish = curr_row['Close'] < curr_row['Open'] and curr_row['Close'] < prev_prev_row['Close']
        
        return first_bearish and small_bullish and final_bearish

    def is_three_inside_down(self, prev_prev_row, prev_row, curr_row):
        # Bearish reversal pattern
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        second_bearish = prev_row['Close'] < prev_row['Open']
        third_bearish = curr_row['Close'] < curr_row['Open']
        
        return (first_bullish and second_bearish and third_bearish and
                prev_row['Open'] < prev_prev_row['Close'] and prev_row['Close'] > prev_prev_row['Open'] and
                curr_row['Close'] < prev_prev_row['Open'])
    def is_dark_cloud_cover(self,prev_row, curr_row):
        first_bullish = prev_row['Close'] > prev_row['Open']
        second_bearish = curr_row['Close'] < curr_row['Open']
        open_above_prev_high = curr_row['Open'] > prev_row['High']
        prev_midpoint = (prev_row['Open'] + prev_row['Close']) / 2
        close_below_prev_mid = curr_row['Close'] < prev_midpoint
        return first_bullish and second_bearish and open_above_prev_high and close_below_prev_mid

    def is_three_white_soldiers(self,prev_prev_row, prev_row, curr_row):
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        second_bullish = prev_row['Close'] > prev_row['Open']
        third_bullish = curr_row['Close'] > curr_row['Open']
        return (first_bullish and second_bullish and third_bullish and
                prev_row['Open'] < prev_prev_row['Close'] and curr_row['Open'] < prev_row['Close'] and
                prev_row['Close'] > prev_prev_row['Close'] and curr_row['Close'] > prev_row['Close'])

    def is_three_black_crows(self, prev_prev_row, prev_row, curr_row):
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        second_bearish = prev_row['Close'] < prev_row['Open']
        third_bearish = curr_row['Close'] < curr_row['Open']
        return (first_bearish and second_bearish and third_bearish and
                prev_row['Open'] > prev_prev_row['Close'] and curr_row['Open'] > prev_row['Close'] and
                prev_row['Close'] < prev_prev_row['Close'] and curr_row['Close'] < prev_row['Close'])
    




    async def get_candle_streak(self, ticker, headers=None):
        """Returns the streak and trend (up or down) for each timespan, along with the ticker"""
        
        async def calculate_streak(ticker, interval, data):
            """Helper function to calculate the streak and trend for a given dataset"""
            # Conversion dictionary to map intervals to human-readable timespans
            conversion = { 
                'm1': '1min',
                'm5': '5min',
                'm30': '30min',
                'm60': '1h',
                'm120': '2h',
                'm240': '4h',
                'd': 'day',
                'w': 'week',
                'm': 'month'
            }

            # Initialize variables
            streak_type = None
            streak_length = 1  # Starting with 1 since the most recent candle is part of the streak

            # Start from the most recent candle and scan forward through the data
            for i in range(1, len(data)):
                current_open = data['Open'].iloc[i]
                current_close = data['Close'].iloc[i]

                # Determine if the candle is green (up) or red (down)
                if current_close > current_open:
                    current_streak_type = 'up'
                elif current_close < current_open:
                    current_streak_type = 'down'
                else:
                    break  # Stop if the candle is neutral (no movement)

                if streak_type is None:
                    streak_type = current_streak_type  # Set initial streak type
                elif streak_type != current_streak_type:
                    break  # Break if the trend changes (from up to down or vice versa)

                streak_length += 1

            if streak_type is None:
                return {f"streak_{conversion[interval]}": 0, f"trend_{conversion[interval]}": "no trend"}

            return {f"streak_{conversion[interval]}": streak_length, f"trend_{conversion[interval]}": streak_type}


        try:
            # Define the intervals of interest
            intervals = ['d', 'w', 'm', 'm5', 'm30', 'm60', 'm120', 'm240']  # Choose 4h, day, and week for your example

            # Fetch the data asynchronously for all intervals
            # Fetch the data asynchronously for all intervals
            data_list = await asyncio.gather(
                *[self.get_candle_data(ticker=ticker, interval=interval, headers=headers, count=200) for interval in intervals]
            )

            # Process each interval's data and gather the streak and trend
            streak_data = {}
            for interval, data in zip(intervals, data_list):
                result = await calculate_streak(ticker, interval, data)
                streak_data.update(result)  # Add the streak and trend for each timespan

            # Add the ticker to the result
            streak_data["ticker"] = ticker

            return streak_data

        except Exception as e:
            print(f"{ticker}: {e}")
            return None



    def classify_candle(self,open_value, close_value):
        if close_value > open_value:
            return "green"
        elif close_value < open_value:
            return "red"
        else:
            return "neutral"

    # Function to classify candle colors across all intervals
    def classify_candle_set(self,opens, closes):
        return [self.classify_candle(open_val, close_val) for open_val, close_val in zip(opens, closes)]

    # Function to classify shapes across rows for one set of rows
    def classify_shape(self,open_val, high_val, low_val, close_val, color, interval, ticker):
        body = abs(close_val - open_val)
        upper_wick = high_val - max(open_val, close_val)
        lower_wick = min(open_val, close_val) - low_val
        total_range = high_val - low_val

        if total_range == 0:
            return None  # Skip if there's no valid data

        body_percentage = (body / total_range) * 100
        upper_wick_percentage = (upper_wick / total_range) * 100
        lower_wick_percentage = (lower_wick / total_range) * 100

        if body_percentage < 10 and upper_wick_percentage > 45 and lower_wick_percentage > 45:
            return f"Doji ({color}) - {ticker} [{interval}]"
        elif body_percentage > 60 and upper_wick_percentage < 20 and lower_wick_percentage < 20:
            return f"Long Body ({color}) - {ticker} [{interval}]"
        elif body_percentage < 30 and lower_wick_percentage > 50:
            return f"Hammer ({color}) - {ticker} [{interval}]" if color == "green" else f"Hanging Man ({color}) - {ticker} [{interval}]"
        elif body_percentage < 30 and upper_wick_percentage > 50:
            return f"Inverted Hammer ({color}) - {ticker} [{interval}]" if color == "green" else f"Shooting Star ({color}) - {ticker} [{interval}]"
        elif body_percentage < 50 and upper_wick_percentage > 20 and lower_wick_percentage > 20:
            return f"Spinning Top ({color}) - {ticker} [{interval}]"
        else:
            return f"Neutral ({color}) - {ticker} [{interval}]"

    # Function to classify candle shapes across all intervals for a given ticker
    def classify_candle_shapes(self, opens, highs, lows, closes, colors, intervals, ticker):
        return [self.classify_shape(open_val, high_val, low_val, close_val, color, interval, ticker)
                for open_val, high_val, low_val, close_val, color, interval in zip(opens, highs, lows, closes, colors, intervals)]



    async def get_candle_patterns(self, ticker:str='AAPL', interval:str='m60', headers=None):

        # Function to compare two consecutive candles and detect patterns like engulfing and tweezers
        def compare_candles(open1, close1, high1, low1, color1, open2, close2, high2, low2, color2, interval, ticker):
            conversion = { 
                'm1': '1min',
                'm5': '5min',
                'm30': '30min',
                'm60': '1h',
                'm120': '2h',
                'm240': '4h',
                'd': 'day',
                'w': 'week',
                'm': 'month'
            }

            # Bullish Engulfing
            if color1 == "red" and color2 == "green" and open2 < close1 and close2 > open1:
                candle_pattern = f"Bullish Engulfing - {ticker} {conversion.get(interval)}"
                return candle_pattern
            # Bearish Engulfing
            elif color1 == "green" and color2 == "red" and open2 > close1 and close2 < open1:
                candle_pattern = f"Bearish Engulfing - {conversion.get(interval)}"
                return candle_pattern
            # Tweezer Top
            elif color1 == "green" and color2 == "red" and high1 == high2:
                candle_pattern = f"Tweezer Top - {conversion.get(interval)}"
                return candle_pattern
            # Tweezer Bottom
            elif color1 == "red" and color2 == "green" and low1 == low2:
                candle_pattern = f"tweezer_bottom"
                return candle_pattern
            
    
        try:
            df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)
            df = df[::-1]

            color1 = 'red' if df['Open'].loc[0] > df['Close'].loc[0] else 'green' if df['Close'].loc[0] > df['Open'].loc[0] else 'grey'
            color2 = 'red' if df['Open'].loc[1] > df['Close'].loc[1] else 'green' if df['Close'].loc[1] > df['Open'].loc[1] else 'grey'




            candle_pattern = compare_candles(close1=df['Close'].loc[0], close2=df['Close'].loc[1], high1=df['High'].loc[0], high2=df['High'].loc[1], low1=df['Low'].loc[0], low2=df['Low'].loc[1], open1=df['Open'].loc[0], open2=df['Open'].loc[1], color1=color1, color2=color2, interval=interval, ticker=ticker)
            if candle_pattern is not []:
                dict = { 
                    'ticker': ticker,
                    'interval': interval,
                    'shape': candle_pattern
                }

                df = pd.DataFrame(dict, index=[0])
                if df['shape'] is not None:
                    return df
        except Exception as e:
            print(e)


    async def ta_bollinger(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the ease_of_movement indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month

        ARGS:
        window: default 14
        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker, interval, headers=headers)
                
            boll_hband = ta.volatility.bollinger_hband(close=df['Close'].astype(float), fillna=True)
            boll_lband = ta.volatility.bollinger_lband(close=df['Close'].astype(float), fillna=True)
            boll_pband = ta.volatility.bollinger_pband(close=df['Close'].astype(float), fillna=True)
            boll_wband = ta.volatility.bollinger_wband(close=df['Close'].astype(float), fillna=True)
            boll_mavg = ta.volatility.bollinger_mavg(close=df['Close'].astype(float), fillna=True)
        

            df['boll_wband'] = boll_wband
            df['boll_hband'] = boll_hband
            df['boll_lband'] = boll_lband
            df['boll_pband'] = boll_pband
            df['boll_mavg'] = boll_mavg

            
            return df
        except Exception as e:
            print(e)


    async def ta_donchain(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the ease_of_movement indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker, interval, headers=headers)
                
            donchain_hband = ta.volatility.donchian_channel_hband(high=df['High'].astype(float), low=df['Low'].astype(float), close=df['Close'].astype(float), fillna=True)
            donchain_lband = ta.volatility.donchian_channel_lband(high=df['High'].astype(float), low=df['Low'].astype(float), close=df['Close'].astype(float), fillna=True)
            donchain_pband=ta.volatility.donchian_channel_pband(high=df['High'].astype(float), low=df['Low'].astype(float), close=df['Close'].astype(float), fillna=True)
            donchain_mband = ta.volatility.donchian_channel_mband(high=df['High'].astype(float), low=df['Low'].astype(float), close=df['Close'].astype(float), fillna=True)
            donchain_wband = ta.volatility.donchian_channel_wband(high=df['High'].astype(float), low=df['Low'].astype(float), close=df['Close'].astype(float), fillna=True)

            df['donchain_hband'] = donchain_hband
            df['donchain_lband'] = donchain_lband
            df['donchain_midband'] = donchain_mband
            df['donchain_pctband'] = donchain_pband
            df['donchain_wband'] = donchain_wband
            
            return df
        except Exception as e:
            print(e)

    async def ta_kelter_channel(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the ease_of_movement indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            kelter_hband = ta.volatility.keltner_channel_hband(high=df['High'].astype(float), low=df['Low'].astype(float), close=df['Close'].astype(float), fillna=True)
            kelter_lband = ta.volatility.keltner_channel_lband(high=df['High'].astype(float), low=df['Low'].astype(float), close=df['Close'].astype(float), fillna=True)
            kelter_mavg = ta.volatility.keltner_channel_mband(high=df['High'].astype(float), close=df['Close'].astype(float), low=df['Low'].astype(float), fillna=True)
            kelter_pband = ta.volatility.keltner_channel_pband(high=df['High'].astype(float), close=df['Close'].astype(float), low=df['Low'].astype(float), fillna=True)
            kelter_wband = ta.volatility.keltner_channel_wband(high=df['High'].astype(float), close=df['Close'].astype(float), low=df['Low'].astype(float), fillna=True)


            df['kelter_hband'] = kelter_hband
            df['kelter_lband'] = kelter_lband
            df['kelter_mavg'] = kelter_mavg
            df['kelter_pctband'] = kelter_pband
            df['kelter_wband'] = kelter_wband

            
            return df
        except Exception as e:
            print(e)


    async def ta_awesome_oscillator(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the ease_of_movement indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            awesome_oscillator = ta.momentum.awesome_oscillator(high=df['High'].astype(float), low=df['Low'].astype(float), fillna=True)

            df['awesome_oscillator'] = awesome_oscillator

            
            return df
        except Exception as e:
            print(e)



    async def ta_kama(self, headers, ticker:str, interval:str='m60'):
        """Moving average designed to account for market noise or volatility. KAMA will closely follow prices when the price swings are relatively small and the noise is low. KAMA will adjust when the price swings widen and follow prices from a greater distance. This trend-following indicator can be used to identify the overall trend, time turning points and filter price movements.
        
        
        
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)
            

            kama = ta.momentum.kama(close=df['Close'].astype(float), fillna=True)


            df['kama'] = kama


            return df
        except Exception as e:
            print(e)


    async def ta_ppo(self, headers, ticker:str, interval:str='m60'):
        """The Percentage Price Oscillator (PPO) is a momentum oscillator that measures the difference between two moving averages as a percentage of the larger moving average.

        https://school.stockcharts.com/doku.php?id=technical_indicators:price_oscillators_ppo
                
        
        
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)
            

            ppo = ta.momentum.ppo(df['Close'], fillna=True)

            ppo_hist = ta.momentum.ppo_hist(df['Close'].astype(float), fillna=True)

            ppo_signal = ta.momentum.ppo_signal(df['Close'].astype(float), fillna=True)


            df['ppo'] = ppo
            df['ppo_hist'] = ppo_hist
            df['ppo_signal'] = ppo_signal

            return df
        except Exception as e:
            print(e)


    async def ta_stoch(self, headers, ticker:str, interval:str='m60'):
        """Developed in the late 1950s by George Lane. The stochastic oscillator presents the location of the closing price of a stock in relation to the high and low range of the price of a stock over a period of time, typically a 14-day period.

        https://www.investopedia.com/terms/s/stochasticoscillator.asp
                        
                
        
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)
            

            stoch = ta.momentum.stoch(high=df['High'].astype(float), low=df['Low'].astype(float), close=df['Close'].astype(float), fillna=True)
            stoch_signal = ta.momentum.stoch_signal(high=df['High'].astype(float), low=df['Low'].astype(float), close=df['Close'].astype(float), fillna=True)

            df['stoch'] = stoch
            df['stoch_signal'] = stoch_signal



            return df
        except Exception as e:
            print(e)


    async def ta_tsi(self, headers, ticker:str, interval:str='m60'):
        """Shows both trend direction and overbought/oversold conditions.

        https://en.wikipedia.org/wiki/True_strength_index
                                
                
        
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)
            

            tsi = ta.momentum.tsi(close=df['Close'].astype(float), fillna=True)

            df['tsi'] = tsi

            return df
        except Exception as e:
            print(e)

    async def ta_williamsr(self, headers, ticker:str, interval:str='m60'):
        """Developed by Larry Williams, Williams %R is a momentum indicator that is the inverse of the Fast Stochastic Oscillator. Also referred to as %R, Williams %R reflects the level of the close relative to the highest high for the look-back period. In contrast, the Stochastic Oscillator reflects the level of the close relative to the lowest low. %R corrects for the inversion by multiplying the raw value by -100. As a result, the Fast Stochastic Oscillator and Williams %R produce the exact same lines, only the scaling is different. Williams %R oscillates from 0 to -100.

        Readings from 0 to -20 are considered overbought. Readings from -80 to -100 are considered oversold.

        Unsurprisingly, signals derived from the Stochastic Oscillator are also applicable to Williams %R.

        %R = (Highest High - Close)/(Highest High - Lowest Low) * -100

        Lowest Low = lowest low for the look-back period Highest High = highest high for the look-back period %R is multiplied by -100 correct the inversion and move the decimal.

        From: https://www.investopedia.com/terms/w/williamsr.asp The Williams %R oscillates from 0 to -100. When the indicator produces readings from 0 to -20, this indicates overbought market conditions. When readings are -80 to -100, it indicates oversold market conditions.
                                        
                
        
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)
            

            williams_r = ta.momentum.williams_r(high=df['High'].astype(float), low=df['Low'].astype(float), close=df['Close'].astype(float), fillna=True)

            df['williams_r'] = williams_r

            return df
        except Exception as e:
            print(e)


    async def ta_macd(self, headers, ticker:str, interval:str='m60'):
        """
        
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)
            
            macd= ta.trend.macd(close=df['Close'].astype(float), fillna=True)
            macd_diff = ta.trend.macd_diff(close=df['Close'].astype(float), fillna=True)
            macd_signal = ta.trend.macd_signal(close=df['Close'].astype(float), fillna=True)


            df['macd'] = macd
            df['macd_diff'] = macd_diff
            df['macd_signal'] = macd_signal

            return df
        except Exception as e:
            print(e)




    async def ta_vortex(self, headers, ticker:str, interval:str='m60'):
        """
        It consists of two oscillators that capture positive and negative trend movement. A bearish signal triggers when the negative trend indicator crosses above the positive trend indicator or a key level.


        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)
            
            vortex_neg = ta.trend.vortex_indicator_neg(high=df['High'].astype(float), low=df['Low'].astype(float), close=df['Close'].astype(float), fillna=True)
            vortex_pos = ta.trend.vortex_indicator_pos(high=df['High'].astype(float), low=df['Low'].astype(float), close=df['Close'].astype(float), fillna=True)
            df['vortex_pos'] = vortex_pos
            df['vortex_neg'] = vortex_neg
            return df
        except Exception as e:
            print(e)


    async def ta_cumulative_return(self, headers, ticker:str, interval:str='m60'):
        """

        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)
            df['High'] = df['High'].astype(float)
            df['Close'] = df['Close'].astype(float)
            cum = ta.others.cumulative_return(close=df['Close'], fillna=True)

            df['cum_return'] = cum
            return df
        except Exception as e:
            print(e)

    async def ta_aroon(self, ticker, timespan, headers, window:int=25):
        """
        Asynchronously calculate the Aroon Up and Aroon Down indicators, starting from the most recent candle,
        and scan for bullish or bearish signals based on extreme Aroon values.
        
        Parameters:
        df (DataFrame): DataFrame containing 'High', 'Low', and 'Timestamp' columns.
        period (int): The number of periods to look back for the highest high and lowest low.
        
        Returns:
        DataFrame: DataFrame with added 'Aroon_Up', 'Aroon_Down', and 'Signal' columns.
        """
        try:
            df = await self.get_candle_data(ticker=ticker, interval=timespan, headers=headers)

            aroon_down = ta.trend.aroon_down(df['High'],df['Low'], window=window, fillna=False)
            aroon_up = ta.trend.aroon_up(df['High'], df['Low'], window=window, fillna=True)
            
            df['aroon_up'] = aroon_up
            df['aroon_down'] = aroon_down

            return df
        except Exception as e:
            print(e)




    async def ta_stochrsi(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the stochrsi indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            stochrsi = ta.momentum.stochrsi(close=df['Close'].astype(float), fillna=True)
            stochrsi_d = ta.momentum.stochrsi_d(close=df['Close'].astype(float), fillna=True)
            stochrsi_k = ta.momentum.stochrsi_k(close=df['Close'].astype(float), fillna=True)


            df['stochrsi'] = stochrsi
            df['stochrsi_d'] = stochrsi_d
            df['stochrsi_k'] = stochrsi_k


            
            return df
        except Exception as e:
            print(e)


    async def ta_rate_of_change(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the rate of change indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            roc = ta.momentum.roc(close=df['Close'].astype(float), fillna=True)


            df['roc'] = roc



            
            return df
        except Exception as e:
            print(e)


    async def ta_ultimate_oscillator(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the ultimate oscillator indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            ultimate_oscillator = ta.momentum.ultimate_oscillator(close=df['Close'].astype(float),high=df['High'].astype(float),low = df['Low'].astype(float),  fillna=True)


            df['ultimate_oscillator'] = ultimate_oscillator



            
            return df
        except Exception as e:
            print(e)



    async def ta_adx(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the adx indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            adx = ta.trend.adx(close=df['Close'].astype(float),high=df['High'].astype(float),low = df['Low'].astype(float),  fillna=True)
            adx_neg = ta.trend.adx_neg(close=df['Close'].astype(float),high=df['High'].astype(float),low = df['Low'].astype(float),  fillna=True)
            adx_pos = ta.trend.adx_pos(close=df['Close'].astype(float),high=df['High'].astype(float),low = df['Low'].astype(float),  fillna=True)


            df['adx'] = adx
            df['adx_neg'] = adx_neg
            df['adx_pos'] = adx_pos


            
            return df
        except Exception as e:
            print(e)


    async def ta_cci(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the cci indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            cci = ta.trend.cci(close=df['Close'].astype(float),high=df['High'].astype(float),low = df['Low'].astype(float),  fillna=True)

            df['cci'] = cci



            
            return df
        except Exception as e:
            print(e)


    async def ta_dpo(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the dpo indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            dpo = ta.trend.dpo(close=df['Close'].astype(float),  fillna=True)

            df['dpo'] = dpo



            
            return df
        except Exception as e:
            print(e)



    async def ta_ichomoku(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the ta_ichomoku indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            ichimoku_a = ta.trend.ichimoku_a(high=df['High'].astype(float),low=df['Low'].astype(float),  fillna=True)
            ichimoku_b = ta.trend.ichimoku_b(high=df['High'].astype(float),low=df['Low'].astype(float),  fillna=True)
            ichimoku_baseline = ta.trend.ichimoku_base_line(high=df['High'].astype(float),low=df['Low'].astype(float),  fillna=True)
            ichimoku_conversionline = ta.trend.ichimoku_conversion_line(high=df['High'].astype(float),low=df['Low'].astype(float),  fillna=True)

            df['ichimoku_a'] = ichimoku_a
            df['ichimoku_b'] = ichimoku_b
            df['ichimoku_baseline'] = ichimoku_baseline
            df['ichimoku_conversionline'] = ichimoku_conversionline



            
            return df
        except Exception as e:
            print(e)



    async def ta_psar(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the psar indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            psar_down = ta.trend.psar_down(high=df['High'].astype(float),low=df['Low'].astype(float), close=df['Close'].astype(float),  fillna=True)
            psar_up = ta.trend.psar_up(high=df['High'].astype(float),low=df['Low'].astype(float), close=df['Close'].astype(float),  fillna=True)

            df['psar_down'] = psar_down
            df['psar_up'] = psar_up

            
            return df
        except Exception as e:
            print(e)



    async def ta_trix(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the trix indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            trix = ta.trend.trix(close=df['Close'].astype(float),  fillna=True)

            df['trix'] = trix
            
            return df
        except Exception as e:
            print(e)


    async def ta_daily_log_return(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the daily log return indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            daily_log_return = ta.others.daily_log_return(close=df['Close'].astype(float),  fillna=True)

            df['daily_log_return'] = daily_log_return
            
            return df
        except Exception as e:
            print(e)



    async def ta_pvo(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the pvo indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            pvo = ta.momentum.pvo(close=df['Volume'].astype(float),  fillna=True)
            pvo_hist = ta.momentum.pvo_hist(close=df['Volume'].astype(float),  fillna=True)
            pvo_signal = ta.momentum.pvo_signal(close=df['Volume'].astype(float),  fillna=True)

            df['pvo'] = pvo
            df['pvo_hist'] = pvo_hist
            df['pvo_signal'] = pvo_signal
            
            return df
        except Exception as e:
            print(e)


    async def ta_kst(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the kst indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.get_candle_data(ticker=ticker, interval=interval, headers=headers)


            kst = ta.trend.kst(close=df['Close'].astype(float), fillna=True)
            kst_signal = ta.trend.kst_sig(close=df['Close'].astype(float), fillna=True)

            df['kst'] = kst
            df['kst_signal'] = kst_signal
            
            return df
        except Exception as e:
            print(e)


    def rank_adx_signal(self,adx, adx_neg, adx_pos):
        """
        Rank the ADX signal based on the values of ADX, adx_neg (-DI), and adx_pos (+DI).
        """
        if adx < 20:
            return "weak trend"
        if adx_neg > adx_pos:
            if adx >= 25:
                return "strong bearish"
            else:
                return "bearish"
        elif adx_pos > adx_neg:
            if adx >= 25:
                return "strong bullish"
            else:
                return "bullish"
        else:
            return "neutral"

    def rank_aroon_signal(self,aroon_up, aroon_down):
        """
        Rank the Aroon signal based on the values of aroon_up and aroon_down.
        """
        if aroon_up > 70 and aroon_down < 30:
            return "strong bullish"
        elif aroon_down > 70 and aroon_up < 30:
            return "strong bearish"
        elif aroon_up > 50 and aroon_down < 50:
            return "bullish"
        elif aroon_down > 50 and aroon_up < 50:
            return "bearish"
        else:
            return "neutral"

    def rank_donchian_signal(self,close_price, donchian_upper_band, donchian_lower_band):
        """
        Rank the Donchian Channel signal based on the close price and the Donchian bands.
        """
        if close_price > donchian_upper_band:
            return "bullish breakout"
        elif close_price < donchian_lower_band:
            return "bearish breakout"
        else:
            return "neutral"

    def rank_keltner_signal(self,close_price, keltner_upper_band, keltner_lower_band):
        """
        Rank the Keltner Channel signal based on the close price and the Keltner bands.
        """
        if close_price > keltner_upper_band:
            return "bullish breakout"
        elif close_price < keltner_lower_band:
            return "bearish breakout"
        else:
            return "neutral"

    def rank_ppo_signal(self,ppo, ppo_signal):
        """
        Rank the PPO signal based on PPO and its signal line.
        """
        if ppo > ppo_signal:
            return "bullish"
        elif ppo < ppo_signal:
            return "bearish"
        else:
            return "neutral"

    def rank_ichimoku_signal(self,close_price, conversion_line, base_line, span_a, span_b):
        """
        Rank the Ichimoku signal based on price and Ichimoku components.
        """
        if close_price > max(span_a, span_b):
            if conversion_line > base_line:
                return "strong bullish"
            else:
                return "bullish"
        elif close_price < min(span_a, span_b):
            if conversion_line < base_line:
                return "strong bearish"
            else:
                return "bearish"
        else:
            return "neutral"

    def rank_dpo_signal(self,dpo):
        """
        Rank the Detrended Price Oscillator (DPO) signal.
        """
        if dpo > 0:
            return "bullish"
        elif dpo < 0:
            return "bearish"
        else:
            return "neutral"

    def rank_ao_signal(self,ao):
        """
        Rank the Awesome Oscillator (AO) signal.
        """
        if ao > 0:
            return "bullish"
        elif ao < 0:
            return "bearish"
        else:
            return "neutral"

    def rank_kama_signal(self,close_price, kama):
        """
        Rank the Kaufman's Adaptive Moving Average (KAMA) signal.
        """
        if close_price > kama:
            return "bullish"
        elif close_price < kama:
            return "bearish"
        else:
            return "neutral"

    def rank_psar_signal(self,psar, close_price):
        """
        Rank the Parabolic SAR (PSAR) signal.
        """
        if psar < close_price:
            return "bullish"
        elif psar > close_price:
            return "bearish"
        else:
            return "neutral"

    def rank_tsi_signal(self,tsi):
        """
        Rank the True Strength Index (TSI) signal.
        """
        if tsi > 0:
            return "bullish"
        elif tsi < 0:
            return "bearish"
        else:
            return "neutral"

    def rank_trix_signal(self,trix):
        """
        Rank the TRIX indicator signal.
        """
        if trix > 0:
            return "bullish"
        elif trix < 0:
            return "bearish"
        else:
            return "neutral"

    def rank_bollinger_signal(self,close_price, upper_band, lower_band):
        """
        Rank the Bollinger Bands signal.
        """
        if close_price > upper_band:
            return "overbought"
        elif close_price < lower_band:
            return "oversold"
        else:
            return "neutral"

    def rank_cci_signal(self,cci):
        """
        Rank the Commodity Channel Index (CCI) signal.
        """
        if cci > 100:
            return "overbought"
        elif cci < -100:
            return "oversold"
        else:
            return "neutral"

    def rank_roc_signal(self,roc):
        """
        Rank the Rate of Change (ROC) signal.
        """
        if roc > 0:
            return "bullish"
        elif roc < 0:
            return "bearish"
        else:
            return "neutral"

    def rank_stochrsi_signal(self,k, d):
        """
        Rank the Stochastic RSI signal.
        """
        if k > 80 and d > 80:
            return "overbought"
        elif k < 20 and d < 20:
            return "oversold"
        else:
            return "neutral"

    def rank_stoch_signal(self,k, d):
        """
        Rank the Stochastic Oscillator signal.
        """
        if k > 80 and d > 80:
            return "overbought"
        elif k < 20 and d < 20:
            return "oversold"
        else:
            return "neutral"

    def rank_ultimate_oscillator_signal(self,uo):
        """
        Rank the Ultimate Oscillator signal.
        """
        if uo > 70:
            return "overbought"
        elif uo < 30:
            return "oversold"
        else:
            return "neutral"

    def rank_vortex_signal(self,vortex_pos, vortex_neg):
        """
        Rank the Vortex Indicator signal.
        """
        if vortex_pos > vortex_neg:
            return "bullish"
        elif vortex_neg > vortex_pos:
            return "bearish"
        else:
            return "neutral"

    async def get_ta_signals(self, ticker, interval, close_price):
    
        try:
            # Fetch data
            headers = {}  # Your headers here

            # Create tasks for concurrent execution
            tasks = [
                self.ta_adx(ticker=ticker, interval=interval, headers=headers),
                self.ta_aroon(ticker=ticker, timespan=interval, headers=headers),
                self.ta_donchain(ticker=ticker, interval=interval, headers=headers),
                self.ta_kelter_channel(ticker=ticker, interval=interval, headers=headers),
                self.ta_ppo(ticker=ticker, interval=interval, headers=headers),
                self.ta_ichomoku(ticker=ticker, interval=interval, headers=headers),
                self.ta_dpo(ticker=ticker, interval=interval, headers=headers),
                self.ta_awesome_oscillator(ticker=ticker, interval=interval, headers=headers),
                self.ta_kama(ticker=ticker, interval=interval, headers=headers),
                self.ta_psar(ticker=ticker, interval=interval, headers=headers),
                self.ta_tsi(ticker=ticker, interval=interval, headers=headers),
                self.ta_trix(ticker=ticker, interval=interval, headers=headers),
                self.ta_bollinger(ticker=ticker, interval=interval, headers=headers),
                self.ta_cci(ticker=ticker, interval=interval, headers=headers),
                self.ta_rate_of_change(ticker=ticker, interval=interval, headers=headers),
                self.ta_stoch(ticker=ticker, interval=interval, headers=headers),
                self.ta_stochrsi(ticker=ticker, interval=interval, headers=headers),
                self.ta_vortex(ticker=ticker, interval=interval, headers=headers),
                self.ta_ultimate_oscillator(ticker=ticker, interval=interval, headers=headers),

            ]

            # Run tasks concurrently and gather results
            (
                adx,
                aroon,
                donchian,
                keltner,
                ppo,
                ichimoku,
                dpo,
                ao,
                kama,
                psar,
                tsi,
                trix,
                boll,
                cci,
                roc,
                stoch,
                stochrsi,
                vortex,
                ultimate,
            ) = await asyncio.gather(*tasks)

            # Extract the latest data
            latest_adx = adx.iloc[-1]
            latest_aroon = aroon.iloc[-1]
            latest_donchian = donchian.iloc[-1]
            latest_keltner = keltner.iloc[-1]
            latest_ppo = ppo.iloc[-1]
            latest_ichimoku = ichimoku.iloc[-1]
            latest_dpo = dpo.iloc[-1]
            latest_ao = ao.iloc[-1]
            latest_kama = kama.iloc[-1]
            latest_tsi = tsi.iloc[-1]
            latest_trix = trix.iloc[-1]
            latest_boll = boll.iloc[-1]
            latest_cci = cci.iloc[-1]
            latest_roc = roc.iloc[-1]
            latest_stoch = stoch.iloc[-1]
            latest_stochrsi = stochrsi.iloc[-1]
            latest_vortex = vortex.iloc[-1]
            latest_ultimate = ultimate.iloc[-1]

            # Compute signals
            adx_signal = self.rank_adx_signal(latest_adx['adx'], latest_adx['adx_neg'], latest_adx['adx_pos'])
            aroon_signal = self.rank_aroon_signal(latest_aroon['aroon_up'], latest_aroon['aroon_down'])
            donchian_signal = self.rank_donchian_signal(close_price, latest_donchian['donchain_hband'], latest_donchian['donchain_lband'])
            keltner_signal = self.rank_keltner_signal(close_price, latest_keltner['kelter_hband'], latest_keltner['kelter_lband'])
            ppo_signal = self.rank_ppo_signal(latest_ppo['ppo'], latest_ppo['ppo_signal'])
            ichimoku_signal = self.rank_ichimoku_signal(close_price, latest_ichimoku['ichimoku_conversionline'], latest_ichimoku['ichimoku_baseline'], latest_ichimoku['ichimoku_a'], latest_ichimoku['ichimoku_b'])
            dpo_signal = self.rank_dpo_signal(latest_dpo['dpo'])
            ao_signal = self.rank_ao_signal(latest_ao['awesome_oscillator'])
            kama_signal = self.rank_kama_signal(close_price, latest_kama['kama'])
            tsi_signal = self.rank_tsi_signal(latest_tsi['tsi'])
            trix_signal = self.rank_trix_signal(latest_trix['trix'])
            bollinger_signal = self.rank_bollinger_signal(close_price, latest_boll['boll_hband'], latest_boll['boll_lband'])
            cci_signal = self.rank_cci_signal(latest_cci['cci'])
            roc_signal = self.rank_roc_signal(latest_roc['roc'])
            stoch_signal = self.rank_stoch_signal(latest_stoch['stoch'], latest_stoch['stoch_signal'])
            stochrsi_signal = self.rank_stochrsi_signal(latest_stochrsi['stochrsi_k'], latest_stochrsi['stochrsi_d'])
            vortex_signal = self.rank_vortex_signal(latest_vortex['vortex_pos'], latest_vortex['vortex_neg'])
            ultimate_signal = self.rank_ultimate_oscillator_signal(latest_ultimate['ultimate_oscillator'])

            # Compile all signals
            signals = {
                'adx': adx_signal,
                'aroon': aroon_signal,
                'donchain': donchian_signal,
                'keltner': keltner_signal,
                'ppo': ppo_signal,
                'ichimoku': ichimoku_signal,
                'dpo': dpo_signal,
                'awesome_oscillator': ao_signal,
                'kama': kama_signal,
                'tsi': tsi_signal,
                'trix': trix_signal,
                'bollinger': bollinger_signal,
                'cci': cci_signal,
                'roc': roc_signal,
                'stoch': stoch_signal,
                'stochrsi': stochrsi_signal,
                'vortex': vortex_signal,
                'ultimate_scillator': ultimate_signal,
            }

            df = pd.DataFrame(signals, index=[0])
            interval_dict = {
                'd': 'day',
                'w': 'week',
                'm': 'month'
            }
            df['ticker'] = ticker
            df['timespan'] = interval_dict.get(interval)

            return df
        except Exception as e:
            print(e)

