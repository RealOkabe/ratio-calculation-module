import yfinance as yf
import pandas as pd
from validations import validate_inputs

from typing import Optional


class TickerDataError(Exception):
    """Custom exception for ticker data errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class YfinanceWrapper:
    """
    Wrapper class for Yahoo Finance API.

    Functions:
        get_data: Fetch historical stock data from Yahoo Finance.
        history: Fetch historical stock data from Yahoo Finance.
    """

    def get_data(self, ticker: str, start: str, end: str) -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data from Yahoo Finance.

        Args:
            ticker (str): The stock ticker symbol.
            start (str): The start date for fetching historical data.
            end (str): The end date for fetching historical data.

        Returns:
            pd.DataFrame: The historical stock data.

        Examples:
            >>> data = YfinanceWrapper().get_data("AAPL", "2021-01-01", "2021-12-31")
            >>> print(data)
        """
        try:
            ticker, start, end = validate_inputs(
                ("ticker", ticker, {"type": "str"}),
                ("start", start, {"type": "date"}),
                ("end", end, {"type": "date"}),
            )

            return yf.download(ticker, start=start, end=end)
        except ValueError as e:
            print(f"Value Error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def history(self, ticker: str, start: str, end: str) -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data from Yahoo Finance.

        Args:
            ticker (str): The stock ticker symbol.
            start (str): The start date for fetching historical data.
            end (str): The end date for fetching historical data.

        Returns:
            pd.DataFrame: The historical stock data.

        Examples:
            >>> data = YfinanceWrapper().history("AAPL", "2021-01-01", "2021-12-31")
            >>> print(data)
        """
        try:
            ticker, start, end = validate_inputs(
                ("ticker", ticker, {"type": "str"}),
                ("start", start, {"type": "date"}),
                ("end", end, {"type": "date"}),
            )

            return yf.Ticker(ticker).history(ticker, start=start, end=end)
        except ValueError as e:
            print(f"Value Error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
