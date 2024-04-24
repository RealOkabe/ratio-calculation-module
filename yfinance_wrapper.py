import yfinance as yf
import pandas as pd


class YfinanceWrapper:
    def __init__(self, ticker: str):
        self.ticker = ticker

    def get_data(self, start: str, end: str) -> pd.DataFrame:
        try:
            return yf.download(self.ticker, start=start, end=end)
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
