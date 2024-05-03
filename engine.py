# External Imports
from datetime import datetime
from typing import Any
import sys

# Internal Imports
from ratio_calculator import RatioCalculator
from manager import PortfolioManager, PorfolioJSONError
from validations import validate_input
from yfinance_wrapper import TickerDataError


TOTAL_INVALID_ATTEMPTS = 5


class Engine:
    """
    The Base Engine.

    Functions:
        run: Run the engine.
        ratio_calculator: Run the ratio calculator module.
        run_portfolio_manager: Run the portfolio manager module.
        input: Take input from the user. Validate the input. Exit the engine if too many invalid attempts.
        __mark_invalid_attempt__: Mark an invalid attempt. Exits the engine if too many invalid attempts.
        __exit_engine__: Exit the engine.
    """

    def __init__(self) -> None:
        self.invalid_attempts = 0

    def run(self) -> None:
        """
        Run the engine.
        The user can select a module to run.
        """
        print("\n")
        print("*****************************************")
        print("Welcome to the STOCK ANALYSIS ENGINE")
        print("*****************************************")
        print("This engine allows you to analyze stocks and portfolios.")
        print("\nInstructions:")
        print("Type 'exit' or Ctrl+C at any point of time to exit.")
        print(
            "Type 'quit' to exit the current module or exit engine in module selection.\n"
        )

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
                                "Enter 1 or 2 or quit/exit >> ",
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
                    print("Invalid module. Please try again.\n")
                    self.__mark_invalid_attempt__()
                    self.selector = None

            except EOFError:
                print("Use 'exit' to exit.")
            except KeyboardInterrupt:
                self.__exit_engine__()
            # Any other exceptions will be caught here.
            except Exception as e:
                print(f"Something went wrong: {e}")

    def ratio_calculator(self) -> None:
        """
        Run the ratio calculator module.
        The user can calculate the price-to-earnings ratio for a stock.
        """
        print("\nRatio Calculator")
        print("This module can calculate a few metrics about any ticker.")
        print("Enter 'quit' to exit the module.")
        try:
            ticker = self.input("Enter the ticker: ")

            start = self.input("Enter the start date (yyyy-mm-dd): ", type="date")

            end = self.input("Enter the end date (yyyy-mm-dd): ", optional=True, type="date")
            if not end:
                end = str(datetime.now().date())

            ratio_calculator = RatioCalculator(ticker, start, end)
            while True:
                ratio_to_calculate = self.input(
                        "\n".join(
                            [
                                "What metric would you like to calculate:",
                                "1. Price to Earnings Ratio",
                                "2. Price Change Percentage",
                                "3. Volume Weighted Average Price ",
                                "4. Relative Strength Index",
                                "5. Average True Range",
                                "6. Calculate Everything\n"
                            ]
                        )
                    , type = "int")
                return_value = None
                match ratio_to_calculate:
                    case 1:
                        return_value = ratio_calculator.calculate_pe_ratio()
                    case 2:
                        return_value = ratio_calculator.calculate_pc_percent()
                    case 3:
                        return_value = ratio_calculator.calculate_vwap()
                    case 4:
                        return_value = ratio_calculator.calculate_rsi()
                    case 5:
                        return_value = ratio_calculator.calculate_atr()
                    case 6:
                        return_value = ratio_calculator.calculate_all()
                    case _:
                        print("Please enter a valid value or enter quit/exit\n")
                if return_value is not None:
                    print(return_value)
                to_continue = self.input("Would you like to calculate another metric? Enter 'yes' to continue or 'no' to exit.\n")
                if to_continue == 'yes':
                    continue
                break
        except TickerDataError as e:
            print(f"Error occurred: {e}")
        except EOFError:
            self.selector = None
            print("Exiting ratio calculator.\n")

    def run_portfolio_manager(self) -> None:
        """
        Run the portfolio manager module.
        The user can either load a portfolio from a file or enter stocks manually.
        """

        print("\n***** PORTFOLIO MANAGER *****")
        print("You can either load a portfolio from a file or enter stocks manually.")
        print("Enter 'quit' to exit the module.")
        try:
            print("\nPlots will be saved under /portfolio_analysis folder.")
            print(
                "WARNING: If the folder exists, it will be deleted and recreated. Please save those files if you require there somewhere\n"
            )

            save_report = self.input(
                "Would you also like to save the portfolio analysis report? (yes/no): ",
                type="acceptance",
            )

            path = self.input(
                "Enter the path to the portfolio JSON file\n(leave empty to enter stocks manually): "
            )

            if path:
                manager = PortfolioManager(path)
            else:
                manager = PortfolioManager()
                num_stocks = self.input(
                    "Enter the number of stocks in your portfolio: ", type="int"
                )
                for i in range(num_stocks):
                    ticker = self.input(f"Enter ticker symbol for stock {i+1}: ")
                    buy_date = self.input(
                        f"Enter buy date for {ticker} (YYYY-MM-DD): ", type="date"
                    )
                    buy_price = self.input(
                        f"Enter buy price for {ticker}: ", type="float"
                    )
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
            print("\n")

            if save_report:
                manager.give_report()
                print("--fyi reports are saved under /portfolio_analysis folder.")

            new_analysis = self.input(
                "\nWould you like to analyze another portfolio? (yes/no): ",
                type="acceptance",
            )

            if not new_analysis:
                self.selector = None

        except (PorfolioJSONError, TickerDataError) as e:
            print(f"Error occurred: {e}")
        except EOFError:
            self.selector = None
            print("Exiting portfolio manager.\n")

    def input(self, prompt, **kwargs) -> Any:
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

    def __mark_invalid_attempt__(self) -> None:
        """Mark an invalid attempt. Exits the engine if too many invalid attempts."""

        self.invalid_attempts += 1
        print(
            "Number of valid attempts left: ",
            TOTAL_INVALID_ATTEMPTS - self.invalid_attempts,
        )
        if self.invalid_attempts >= TOTAL_INVALID_ATTEMPTS:
            print("Too many invalid attempts.")
            self.__exit_engine__()
        print("\n")

    def __exit_engine__(self) -> None:
        """Exit the engine."""

        print("\nExiting the engine. See you later.")
        sys.exit()


if __name__ == "__main__":
    engine = Engine()
    engine.run()
