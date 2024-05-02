import yfinance as yf
import pandas as pd
from validations import validate_inputs


class YfinanceWrapper:
    """Wrapper class for Yahoo Finance API."""

    def get_data(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        try:
            ticker, start, end = validate_inputs(
                ("ticker", ticker, {type: "str"}),
                ("start", start, {type: "date"}),
                ("end", end, {type: "date"}),
            )

            return yf.download(ticker, start=start, end=end)
        except ValueError as e:
            print(f"Value Error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def history(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        try:
            ticker, start, end = validate_inputs(
                ("ticker", ticker, {type: "str"}),
                ("start", start, {type: "date"}),
                ("end", end, {type: "date"}),
            )

            return yf.Ticker(ticker).history(self.ticker, start=start, end=end)
        except ValueError as e:
            print(f"Value Error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
