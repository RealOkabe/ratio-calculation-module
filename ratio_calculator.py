from yfinance_wrapper import YfinanceWrapper
import yfinance as yf


class RatioCalculator:
    def __init__(self, ticker: str, start: str, end: str) -> None:
        self.ticker = ticker
        self.data_wrapper = YfinanceWrapper(ticker)
        self.start = start
        self.end = end

    # Calculate price-to-earnings ratio
    def calculate_pe_ratio(self, ticker: str, start: str, end: str):
        ticker_data = yf.Ticker(self.ticker).history(start = self.start, end = self.end)
        avg_price = (ticker_data['Open'] + ticker_data['High'] + ticker_data['Low'] + ticker_data['Close']) / 4
        ticker_data['PE Ratio'] = avg_price / (ticker_data['Close'] - ticker_data['Open'])
        return ticker_data

    # Calculate Price Change percentage
    def calculate_pc_percent(self, ticker: str, start: str, end: str):
        ticker_data = yf.Ticker(self.ticker).history(start = self.start, end = self.end)
        book_price = ticker_data['Close'] - ticker_data['Open']
        ticker_data['Price Change Percentage'] = book_price / ticker_data['Open']
        return ticker_data

    # Calculate volume-weighted average price
    def calculate_vwap(self, ticker: str, start: str, end: str):
        ticker_data = yf.Ticker(self.ticker).history(start = self.start, end = self.end)
        avg_price = (ticker_data['Open'] + ticker_data['High'] + ticker_data['Low'] + ticker_data['Close']) / 4
        vwap = sum(avg_price * ticker_data['Volume']) / sum(ticker_data['Volume'])
        return vwap

    # Calculate Relative Strength Index
    def calculate_rsi(self, ticker: str, start: str, end: str):
        ticker_data = yf.Ticker(self.ticker).history(start = self.start, end = self.end)
        ticker_data['price_diff'] = ticker_data['Close'] - ticker_data['Open']
        up_closes = []
        down_closes = []
        for index, row in ticker_data.iterrows():
            if row['price_diff'] > 0:
                up_closes.append(row['Close'])
            else:
                down_closes.append(row['Close'])
        avg_up_close = sum(up_closes) / len(up_closes)
        avg_down_close = sum(down_closes) / len(down_closes)
        relative_strength = avg_up_close / avg_down_close
        return (100 - (100 / (1 + relative_strength)))

    # Calculate the Average True Range
    def calculate_atr(self, ticker: str, start: str, end: str):
        ticker_data = yf.Ticker(self.ticker).history(start = self.start, end = self.end)
        ticker_data['ATR'] = 0
        prev_close = None
        for i in ticker_data.index:
            if prev_close is None:
                ticker_data['ATR'][i] = ticker_data['High'][i] - ticker_data['Low'][i]
                prev_close = ticker_data['Close'][i]
                continue
            ticker_data['ATR'][i] = max(ticker_data['High'][i] - ticker_data['Low'][i], abs(ticker_data['High'][i] - prev_close), abs(ticker_data['Low'][i] - prev_close))
            prev_close = ticker_data['Close'][i]
        return ticker_data

    