from yfinance_wrapper import YfinanceWrapper
import yfinance as yf


class RatioCalculator:
    def __init__(self, ticker: str, start: str, end: str) -> None:
        self.ticker = ticker
        self.data_wrapper = YfinanceWrapper()
        self.start = start
        self.end = end
        self.ticker_data = self.data_wrapper.history(ticker,
            self.start, self.end
        )

    # Calculate price-to-earnings ratio
    def calculate_pe_ratio(self):
        avg_price = (
            self.ticker_data["Open"]
            + self.ticker_data["High"]
            + self.ticker_data["Low"]
            + self.ticker_data["Close"]
        ) / 4
        self.ticker_data["PE Ratio"] = avg_price / (
            self.ticker_data["Close"] - self.ticker_data["Open"]
        )
        return self.ticker_data

    # Calculate Price Change percentage
    def calculate_pc_percent(self):
        # self.ticker_data = yf.Ticker(self.ticker).history(start = self.start, end = self.end)
        book_price = self.ticker_data["Close"] - self.ticker_data["Open"]
        self.ticker_data["Price Change Percentage"] = (
            book_price / self.ticker_data["Open"]
        )
        return self.ticker_data

    # Calculate volume-weighted average price
    def calculate_vwap(self):
        # self.ticker_data = yf.Ticker(self.ticker).history(start = self.start, end = self.end)
        avg_price = (
            self.ticker_data["Open"]
            + self.ticker_data["High"]
            + self.ticker_data["Low"]
            + self.ticker_data["Close"]
        ) / 4
        vwap = sum(avg_price * self.ticker_data["Volume"]) / sum(
            self.ticker_data["Volume"]
        )
        return vwap

    # Calculate Relative Strength Index
    def calculate_rsi(self):
        # self.ticker_data = yf.Ticker(self.ticker).history(start = self.start, end = self.end)
        self.ticker_data["price_diff"] = (
            self.ticker_data["Close"] - self.ticker_data["Open"]
        )
        up_closes = []
        down_closes = []
        for index, row in self.ticker_data.iterrows():
            if row["price_diff"] > 0:
                up_closes.append(row["Close"])
            else:
                down_closes.append(row["Close"])
        avg_up_close = sum(up_closes) / len(up_closes)
        avg_down_close = sum(down_closes) / len(down_closes)
        relative_strength = avg_up_close / avg_down_close
        return 100 - (100 / (1 + relative_strength))

    # Calculate the Average True Range
    def calculate_atr(self):
        # self.ticker_data = yf.Ticker(self.ticker).history(start = self.start, end = self.end)
        self.ticker_data["ATR"] = 0
        prev_close = None
        for i in self.ticker_data.index:
            if prev_close is None:
                self.ticker_data["ATR"][i] = (
                    self.ticker_data["High"][i] - self.ticker_data["Low"][i]
                )
                prev_close = self.ticker_data["Close"][i]
                continue

            self.ticker_data["ATR"][i] = max(
                self.ticker_data["High"][i] - self.ticker_data["Low"][i],
                abs(self.ticker_data["High"][i] - prev_close),
                abs(self.ticker_data["Low"][i] - prev_close),
            )
            prev_close = self.ticker_data["Close"][i]
        return self.ticker_data
