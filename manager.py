import yfinance as yf
import pandas as pd


def get_stock_data(ticker: str, start_date: str):
    """Fetch historical stock data from Yahoo Finance."""
    stock_data = yf.download(ticker, start=start_date)
    return stock_data


def calculate_portfolio_performance(portfolio):
    portfolio_analysis = {"portfolio": {}}
    total_investment = 0
    total_value = 0
    for stock, data in portfolio.items():
        buy_price = data["buy_price"]
        quantity = data["quantity"]
        stock_data = data["stock_data"]
        current_price = stock_data["Close"][-1]
        total_investment += buy_price * quantity
        total_value += current_price * quantity
        # Calculate profit/loss
        profit_loss = (current_price - buy_price) * quantity
        portfolio_analysis["portfolio"][stock] = {
            "Buy Price": buy_price,
            "Current Price": current_price,
            "Quantity": quantity,
            "Profit/Loss": profit_loss,
        }
    portfolio_analysis["Total"] = {
        "Total Investment": total_investment,
        "Total Value": total_value,
        "Total Profit/Loss": total_value - total_investment,
    }
    return portfolio_analysis


def generate_recommendation(portfolio_analysis: dict) -> dict:
    recommendations = {}

    for stock, data in portfolio_analysis["portfolio"].items():
        buy_price = data["Buy Price"]
        current_price = data["Current Price"]
        if current_price > buy_price:
            recommendations[stock] = "Sell"
        elif current_price < buy_price:
            recommendations[stock] = "Buy/Hold"
        else:
            recommendations[stock] = "Hold"

    return recommendations


def main():
    # Input portfolio details
    portfolio = {}
    num_stocks = int(input("Enter the number of stocks in your portfolio: "))
    for i in range(num_stocks):
        ticker = input(f"Enter ticker symbol for stock {i+1}: ")
        buy_date = input(f"Enter buy date for {ticker} (YYYY-MM-DD): ")
        buy_price = float(input(f"Enter buy price for {ticker}: "))
        quantity = int(input(f"Enter quantity bought for {ticker}: "))
        stock_data = get_stock_data(ticker, buy_date)
        portfolio[ticker] = {
            "buy_price": buy_price,
            "quantity": quantity,
            "stock_data": stock_data,
        }

    # Calculate portfolio performance
    portfolio_analysis = calculate_portfolio_performance(portfolio)

    # Generate recommendations
    recommendations = generate_recommendation(portfolio_analysis)

    # Display portfolio analysis with recommendations
    print("\nPortfolio Analysis with Recommendations:")
    df = pd.DataFrame.from_dict(portfolio_analysis["portfolio"], orient="index")
    df["Recommendation"] = [recommendations[stock] for stock in df.index]
    print(df)


if __name__ == "__main__":
    main()
