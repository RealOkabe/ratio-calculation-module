from yfinance_wrapper import YfinanceWrapper


class RatioCalculator:
    def __init__(self, ticker: str, start: str, end: str) -> None:
        self.ticker = ticker
        self.data_wrapper = YfinanceWrapper(ticker)
        self.start = start
        self.end = end

    # Calculate price-to-earnings ratio
    def calculate_pe_ratio(self) -> float:
        # data = self.data_wrapper.get_data(self.start, self.end)
        # Calculate earnings per share here
        # price_per_share = ????
        # Calculate price per share here
        # earnings_per_share = ????

        # try:
        #     return price_per_share / earnings_per_share
        # except ZeroDivisionError:
        #     return 0

        pass
