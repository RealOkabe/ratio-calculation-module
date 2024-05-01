from ratio_calculator import RatioCalculator
from datetime import datetime


class Engine:
    def __init__(self):
        pass

    def run(self):
        print("Welcome to the Stock Analysis Engine.")
        print("Type 'quit' or Ctrl+C at any point of time to exit.")

        while True:
            try:
                if not hasattr(self, "selector"):
                    self.selector = None

                if self.selector is None:
                    self.selector = input(
                        "What module would you like to use: \n1. Ratio Calculator\n2. Plot Creator\nEnter 1 or 2 >> "
                    )
                    if self.selector == "quit":
                        break

                if self.selector == "1":
                    self.ratio_calculator()
                elif self.selector == "2":
                    self.create_plots()
                else:
                    print("Invalid module. Please try again.")
                    self.selector = None

                print("\n")
            except EOFError:
                print("Use 'quit' to exit.")

    def ratio_calculator(self):
        print("\nRatio Calculator")
        try:
            ticker = input("Enter the ticker: ")
            if ticker == "quit":
                raise EOFError

            start = input("Enter the start date (yyyy-mm-dd): ")
            if start == "quit":
                raise EOFError

            end = input("Enter the end date (yyyy-mm-dd): ")
            if not end:
                end = str(datetime.date.today())
            if end == "quit":
                raise EOFError

            ratio_calculator = RatioCalculator(ticker, start, end)

            print(f"Price-to-earnings ratio: {ratio_calculator.calculate_pe_ratio()}")
        except EOFError:
            self.selector = None
            print("Exiting ratio calculator.")

    def create_plots(self):
        print("\nPlot Creator")
        try:
            tickers = input("Enter the list of tickers: ")
            if tickers == "quit":
                raise EOFError

            tickers = tickers.split(",")
            start = input("Enter the start date (yyyy-mm-dd): ")
            if start == "quit":
                raise EOFError

            end = input("Enter the end date (yyyy-mm-dd): ")
            if end == "quit":
                raise EOFError
            if not end:
                end = str(datetime.date.today())

            print(f"Creating plots for {tickers} from {start} to {end}")

            # Create plots here
        except EOFError:
            self.selector = None
            print("Exiting plot creator.")


if __name__ == "__main__":
    engine = Engine()
    engine.run()
