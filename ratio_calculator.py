from yfinance_wrapper import YfinanceWrapper
import yfinance as yf


class RatioCalculator:
    def __init__(self, ticker: str, start: str, end: str) -> None:
        self.ticker = ticker
        self.data_wrapper = YfinanceWrapper(ticker)
        self.start = start
        self.end = end

    # Calculate price-to-earnings ratio
    def calculate_pe_ratio(self, ticker: str, start: str, end: str) -> float:
        ticker_data = yf.Ticker(self.ticker, start = self.start, end = self.end)
        pe_ratio = ticker_data['Close'].iloc[-1] / ticker_data.info['trailingPE']
        return pe_ratio

    # Get the return on equity
    def get_return_on_equity(self, ticker: str):
        ticker_data = yf.Ticker(self.ticker)
        return ticker_data['returnOnEquity']

    # Get the return on assets
    def get_return_on_assets(self, ticker: str):
        ticker_data = yf.Ticker(self.ticker)
        return ticker_data['returnOnAssets']

    