# External Imports
from datetime import datetime
from typing import Dict, Any
import sys

# Internal Imports
from ratio_calculator import RatioCalculator
from manager import PortfolioManager
from validations import validate_input


TOTAL_INVALID_ATTEMPTS = 5


class Engine:
    """The Base Engine."""

    def __init__(self):
        self.invalid_attempts = 0

    def run(self):
        """Run the engine."""

        print("Welcome to the Stock Analysis Engine.")
        print("Type 'exit' or Ctrl+C at any point of time to exit.")
        print(
            "Type 'quit' to exit the current module or exit engine in module selection."
        )
        print("\n")

        while True:
            try:
                if not hasattr(self, "selector"):
                    self.selector = None

                if self.selector is None:
                    self.selector = input(
                        "\n".join(
                            [
                                "What module would you like to use:",
                                "1. Ratio Calculator",
                                "2. Portfolio Manager",
                                "Enter 1 or 2 >> ",
                            ]
                        )
                    )
                    if self.selector == "quit" or self.selector == "exit":
                        self.__exit_engine__()

                if self.selector == "1":
                    self.ratio_calculator()
                elif self.selector == "2":
                    self.run_portfolio_manager()
                else:
                    print("Invalid module. Please try again.")
                    self.__mark_invalid_attempt__()
                    self.selector = None

                print("\n")
            except EOFError:
                print("Use 'quit' to exit.")

    def ratio_calculator(self):
        """Run the ratio calculator module."""

        print("\nRatio Calculator")
        try:
            ticker = self.input("Enter the ticker: ")

            start = self.input("Enter the start date (yyyy-mm-dd): ", type="date")

            end = self.input(
                "Enter the end date (yyyy-mm-dd): ", optional=True, type="date"
            )
            if not end:
                end = str(datetime.date.today())

            ratio_calculator = RatioCalculator(ticker, start, end)

            print(f"Price-to-earnings ratio: {ratio_calculator.calculate_pe_ratio()}")
        except EOFError:
            self.selector = None
            print("Exiting ratio calculator.")

    def run_portfolio_manager(self):
        """Run the portfolio manager module."""

        print("\nPortfolio Manager")
        try:
            manager = PortfolioManager()
            num_stocks = self.input(
                "Enter the number of stocks in your portfolio: ", type="int"
            )
            for i in range(num_stocks):
                ticker = self.input(f"Enter ticker symbol for stock {i+1}: ")
                buy_date = self.input(
                    f"Enter buy date for {ticker} (YYYY-MM-DD): ", type="date"
                )
                buy_price = self.input(f"Enter buy price for {ticker}: ", type="float")
                quantity = self.input(
                    f"Enter quantity bought for {ticker}: ", type="int"
                )

                manager.add_stock(ticker, buy_date, buy_price, quantity)

            # Calculate portfolio performance
            portfolio_analysis = manager.calculate_portfolio_performance()

            # Generate recommendations
            recommendations = manager.generate_recommendation(portfolio_analysis)

            # Display portfolio analysis with recommendations
            print("\nPortfolio Analysis with Recommendations:")
            print(recommendations)
        except EOFError:
            self.selector = None
            print("Exiting portfolio manager.")

    def input(self, prompt, **kwargs):
        """
        Take input from the user. Validate the input. Exit the engine if too many invalid attempts.

        Args:
            prompt (str): The prompt to display to the user.
            **kwargs: Keyword arguments to pass to the validate_input function.
            optional and type are two keyword arguments that can be passed to validate_input.

        Returns:
            Any: The validated input.
        """

        while True:
            if self.invalid_attempts >= TOTAL_INVALID_ATTEMPTS:
                print("Too many invalid attempts. Exiting the engine.")
                sys.exit()

            input_value = input(prompt)

            if input_value == "quit":
                raise EOFError

            if input_value == "exit":
                self.__exit_engine__()

            value, error = validate_input(input_value, **kwargs)

            if not error:
                return value

            print(error)
            self.__mark_invalid_attempt__()

    def __mark_invalid_attempt__(self):
        """Mark an invalid attempt. Exits the engine if too many invalid attempts."""

        self.invalid_attempts += 1
        print(
            "Number of valid attempts left: ",
            TOTAL_INVALID_ATTEMPTS - self.invalid_attempts,
            "\n",
        )
        if self.invalid_attempts >= TOTAL_INVALID_ATTEMPTS:
            print("Too many invalid attempts.\n")
            self.__exit_engine__()

    def __exit_engine__(self):
        """Exit the engine."""

        print("Exiting the engine. See you later.")
        sys.exit()


if __name__ == "__main__":
    engine = Engine()
    engine.run()
