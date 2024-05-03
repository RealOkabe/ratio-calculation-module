import json as j
import os
from pathlib import Path
import shutil
from typing import Optional, Dict, Any, List

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

from yfinance_wrapper import YfinanceWrapper, TickerDataError
from validations import validate_inputs


class PorfolioJSONError(Exception):
    """Custom exception for Portfolio JSON errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class PortfolioManager:
    def __init__(
        self,
        path: Optional[str] = None,
        out_path: Path = Path("portfolio_analysis"),
    ):
        """Initialize the Portfolio Manager.
        Args:
            path (str, optional): Path to the JSON file containing the portfolio data. Defaults to None.
        Raises:
            ValueError: If the JSON data is not in the correct format.

        Example JSON format:
        ```json
        {
            "portfolio": {
                "AAPL": {
                    "buy_date": "2022-08-02",
                    "buy_price": 200,
                    "quantity": 5
                },
                "GOOGL": {
                    "buy_date": "2022-08-02",
                    "buy_price": 2000,
                    "quantity": 2
                }
            }
        }
        """
        self.portfolio = {}
        self.yf_wrapper = YfinanceWrapper()

        self.out_path = out_path
        # Delete the existing directory and create a new one
        if os.path.exists(self.out_path):
            shutil.rmtree(self.out_path, ignore_errors=True)

        os.makedirs(self.out_path, exist_ok=True)
        # check if out_path is a valid path and not a file
        if not self.out_path.is_dir():
            raise ValueError("Invalid output path. Please provide a directory path.")

        if path:
            self.path = path
            self.__get_json_data()
            if self.portfolio is None or not self.portfolio:
                raise PorfolioJSONError(
                    "Could not load portfolio data. Check JSON file."
                )

    def __read_json__(self, file_path):
        """Read JSON data from a file."""
        with open(file_path, "r") as file:
            return j.load(file)

    def __get_json_data(self):
        """Get the JSON data from the file.
        Raises:
            ValueError: If the JSON data is not in the correct format.
        """

        try:
            data = self.__read_json__(self.path)
            if "portfolio" not in data:
                raise ValueError("Invalid JSON format. 'portfolio' key not found.")

            if not data["portfolio"]:
                raise ValueError("Portfolio is empty.")

            if not isinstance(data["portfolio"], dict):
                raise ValueError(
                    "Invalid JSON format. 'portfolio' should be a k/v pair. Check Documentation."
                )

            for stock, details in data["portfolio"].items():
                ticker = stock
                buy_date = details["buy_date"]
                buy_price = details["buy_price"]
                quantity = details["quantity"]
                validate_inputs(
                    ("ticker", ticker, {"type": "str"}),
                    ("buy_date", buy_date, {"type": "date"}),
                    ("buy_price", buy_price, {"type": "float"}),
                    ("quantity", quantity, {"type": "int"}),
                )
                self.add_stock(ticker, buy_date, buy_price, quantity)

            print("Portfolio loaded successfully.")

        except FileNotFoundError:
            print(f"File not found: {self.path}")
        except ValueError as value_error:
            print(value_error)

    def give_report(
        self,
        report_name: str = "analysis",
    ):
        """
        Generate a report for the portfolio and recommendations.
        Args:
            out_path (Path, optional): Path to save the report. Defaults to Path("portfolio_analysis").
            report_name (str, optional): Name of the report. Defaults to "analysis".
        Raises:
            ValueError: If the output path is not a valid directory.
            ValueError: If the portfolio performance or recommendations are not calculated.
        """

        try:
            if not self.portfolio_performance or not self.recommendations:
                raise ValueError(
                    "Portfolio performance or recommendations not calculated."
                )
        except ValueError as value_error:
            print(value_error)
            return

        data = {
            "portfolio": self.portfolio_performance["portfolio"],
            "recommendations": self.recommendations,
        }

        for stock, details in data["portfolio"].items():
            # Save stock data to a CSV file
            stock_data = details["stock_data"]
            stock_data.to_csv(
                f"{self.out_path}/{stock}.csv", index=False, header=True, sep=","
            )
            averages = {
                "Open_avg": stock_data["Open"].mean(),
                "High_avg": stock_data["High"].mean(),
                "Low_avg": stock_data["Low"].mean(),
                "Close_avg": stock_data["Close"].mean(),
                "Adj_Close_avg": stock_data["Adj Close"].mean(),
                "Volume_avg": stock_data["Volume"].mean(),
                "10-day_SMA_avg": stock_data["10-day SMA"].mean(),
                "50-day_SMA_avg": stock_data["50-day SMA"].mean(),
            }

            # Add averages to details dictionary
            details.update(averages)
            details.pop("stock_data", None)

        self.__write_json__(file_path=f"{self.out_path}/{report_name}.json", data=data)

    def __write_json__(self, file_path, data):
        """Write JSON data to a file.
        Args:
            file_path (str): Path to the file to write the JSON data to.
            data (dict): The data to write to the file.
        """
        with open(file_path, "w") as file:
            j.dump(data, file, indent=4)

    def get_stock_data(self, ticker: str, start_date: str):
        """Fetch historical stock data from Yahoo Finance.
        Args:
            ticker (str): Stock ticker symbol.
            start_date (str): Start date for fetching historical data.
        Returns:
            DataFrame: Stock data.
        """
        stock_data = self.yf_wrapper.get_data(
            ticker, start_date, datetime.now().date().strftime("%Y-%m-%d")
        )
        if stock_data is None or stock_data.empty:
            raise TickerDataError(
                f"Stock data not found for {ticker}. Please try again."
            )
        return stock_data

    def add_stock(self, ticker, buy_date, buy_price, quantity):
        """Add a stock to the portfolio.
        Args:
            ticker (str): Stock ticker symbol.
            buy_date (str): Date the stock was bought (YYYY-MM-DD).
            buy_price (float): Price at which the stock was bought.
            quantity (int): Quantity of the stock bought.
        """
        stock_data = self.get_stock_data(ticker, buy_date)
        self.portfolio[ticker] = {
            "buy_price": buy_price,
            "quantity": quantity,
            "stock_data": stock_data,
        }

    def calculate_portfolio_performance(self) -> Dict[str, Any]:
        """Calculate the performance of the portfolio.
        Returns:
            dict: Portfolio analysis.
        """
        portfolio_analysis = {"portfolio": {}}
        total_investment = 0
        total_value = 0
        for stock, data in self.portfolio.items():
            buy_price = data["buy_price"]
            quantity = data["quantity"]
            stock_data = data["stock_data"]
            current_price = stock_data["Close"].tolist()[-1]
            total_investment += buy_price * quantity
            total_value += current_price * quantity
            # Calculate profit/loss
            profit_loss = (current_price - buy_price) * quantity
            portfolio_analysis["portfolio"][stock] = {
                "Buy Price": buy_price,
                "Current Price": current_price,
                "Quantity": quantity,
                "Profit/Loss": profit_loss,
                "stock_data": stock_data,
            }
            self.plot_stock_with_moving_averages(stock_data, stock)

        portfolio_analysis["Total"] = {
            "Total Investment": total_investment,
            "Total Value": total_value,
            "Total Profit/Loss": total_value - total_investment,
        }

        self.portfolio_performance = portfolio_analysis
        return portfolio_analysis

    def calculate_simple_moving_average(self, prices: List, window_size: int) -> float:
        """Calculate the simple moving average of a stock. The window size is the number of days to consider.
        Args:
            prices (list): List of stock prices.
            window_size (int): Number of days to consider for the moving average.
        Returns:
            float: The simple moving average."""
        sma = [
            sum(prices[i : i + window_size]) / window_size
            for i in range(len(prices) - window_size + 1)
        ]
        return sma[-1]

    def generate_recommendation(self, portfolio_analysis: Dict) -> Dict[str, str]:
        """Generate recommendations for the stocks in the portfolio based on a decision rule.
        Args:
            portfolio_analysis (dict): Portfolio analysis data.
        Returns:
            dict: Recommendations for each stock in the portfolio."""
        recommendations = {}
        for stock, data in portfolio_analysis["portfolio"].items():
            # current_price = data["Current Price"]
            buy_price = data["Buy Price"]
            stock_data = data["stock_data"]
            recommendation = self.decision_rule_based_model(stock_data, buy_price)
            recommendations[stock] = recommendation

        self.recommendations = recommendations
        return recommendations

    def decision_rule_based_model(
        self, stock_data: pd.DataFrame, buy_price: int
    ) -> str:
        """Simple decision rule based on moving averages.
        Args:
            stock_data (DataFrame): Stock data.
            buy_price (float): Price at which the stock was bought.
        Returns:
            str: Recommendation to Buy, Sell, or Hold."""
        # Get recent close prices
        close_prices = stock_data["Close"].tolist()
        current_price = close_prices[-1]

        # Calculate simple moving averages
        if len(close_prices) > 50:
            short_sma = self.calculate_simple_moving_average(close_prices, 10)
            long_sma = self.calculate_simple_moving_average(close_prices, 50)
        else:
            return "Hold"

        if short_sma > long_sma and current_price > buy_price:
            return "Buy"
        # Shorter term, the price looks like not going up
        # And the price at when it was bought is higer than the current price
        # WE SELL.
        elif short_sma < long_sma and current_price < buy_price:
            return "Sell"
        else:
            return "Hold"

    def plot_stock_with_moving_averages(self, stock_data: pd.DataFrame, ticker: str):
        """Plot the stock prices with 10-day and 50-day simple moving averages.
        Args:
            stock_data (DataFrame): Stock data.
            ticker (str): Stock ticker symbol."""

        # Calculate moving averages
        stock_data["10-day SMA"] = stock_data["Close"].rolling(window=10).mean()
        stock_data["50-day SMA"] = stock_data["Close"].rolling(window=50).mean()

        # Create the plot
        plt.figure(figsize=(12, 6))
        plt.plot(stock_data["Close"], label=f"{ticker} Close Prices", color="blue")
        plt.plot(stock_data["10-day SMA"], label="10-day SMA", color="green")
        plt.plot(stock_data["50-day SMA"], label="50-day SMA", color="red")

        # Adding labels and title
        plt.title(f"{ticker} Stock Prices and Moving Averages")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)

        filename = f"{ticker}_moving_averages_plot.png"
        plt.savefig(os.path.join(self.out_path, filename))
        plt.close()


def main():

    data = "data.json"
    manager = PortfolioManager(path=data)
    portfolio_analysis = manager.calculate_portfolio_performance()

    # Generate recommendations
    recommendations = manager.generate_recommendation(portfolio_analysis)

    manager.give_report()

    # manager.plot_stock_with_moving_averages()

    # Display portfolio analysis with recommendations
    print("\nPortfolio Analysis with Recommendations:")
    df = pd.DataFrame.from_dict(portfolio_analysis["portfolio"], orient="index")
    df["Recommendation"] = [recommendations[stock] for stock in df.index]
    print(df)


if __name__ == "__main__":
    main()
