import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import json


class PortfolioManager:
    def __init__(self):
        self.portfolio = {}

    def __read_json__(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
        # do rest of the processing

    def get_stock_data(self, ticker: str, start_date: str):
        """Fetch historical stock data from Yahoo Finance."""
        # TODO: try catch required
        stock_data = yf.download(ticker, start=start_date)
        return stock_data

    def add_stock(self, ticker, buy_date, buy_price, quantity):
        stock_data = self.get_stock_data(ticker, buy_date)
        if not stock_data or stock_data.empty:
            print(f"Stock data not found for {ticker}. Please try again.")
            return

        self.portfolio[ticker] = {
            "buy_price": buy_price,
            "quantity": quantity,
            "stock_data": stock_data,
        }

    def calculate_portfolio_performance(self):
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

        return portfolio_analysis

    def calculate_simple_moving_average(self, prices, window_size):
        sma = [
            sum(prices[i : i + window_size]) / window_size
            for i in range(len(prices) - window_size + 1)
        ]
        return sma[-1]

    def generate_recommendation(self, portfolio_analysis):
        recommendations = {}
        for stock, data in portfolio_analysis["portfolio"].items():
            # current_price = data["Current Price"]
            buy_price = data["Buy Price"]
            stock_data = data["stock_data"]
            recommendation = self.decision_rule_based_model(stock_data, buy_price)
            recommendations[stock] = recommendation
        return recommendations

    def decision_rule_based_model(self, stock_data, buy_price):
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

    def plot_stock_with_moving_averages(self, stock_data, ticker):
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
        plt.show()


def main():
    # Input portfolio details
    # num_stocks = int(input("Enter the number of stocks in your portfolio: "))
    # for i in range(num_stocks):
    #     ticker = input(f"Enter ticker symbol for stock {i+1}: ")
    #     buy_date = input(f"Enter buy date for {ticker} (YYYY-MM-DD): ")
    #     buy_price = float(input(f"Enter buy price for {ticker}: "))
    #     quantity = int(input(f"Enter quantity bought for {ticker}: "))

    #     manager = PortfolioManager()
    #     manager.add_stock(ticker, buy_date, buy_price, quantity)

    manager = PortfolioManager()
    manager.add_stock("AAPL", "2022-08-02", 200, 5)
    # Calculate portfolio performance
    portfolio_analysis = manager.calculate_portfolio_performance()

    # Generate recommendations
    recommendations = manager.generate_recommendation(portfolio_analysis)

    manager.plot_stock_with_moving_averages()

    # Display portfolio analysis with recommendations
    print("\nPortfolio Analysis with Recommendations:")
    df = pd.DataFrame.from_dict(portfolio_analysis["portfolio"], orient="index")
    df["Recommendation"] = [recommendations[stock] for stock in df.index]
    print(df)


if __name__ == "__main__":
    main()
