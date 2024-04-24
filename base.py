from ratio_calculator import RatioCalculator


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
                    self.selector = input("What module would you like to use: ")
                    if self.selector == "quit":
                        break

                if self.selector == "ratio":
                    self.ratio_calculator()
                elif self.selector == "plot":
                    self.create_plots()
                else:
                    print("Invalid module. Please try again.")
                    self.selector = None

                print("\n")
            except EOFError:
                print("Use 'quit' to exit.")

    def ratio_calculator(self):
        try:
            ticker = input("Enter the ticker: ")
            if ticker == "quit":
                raise EOFError

            start = input("Enter the start date (yyyy-mm-dd): ")
            if start == "quit":
                raise EOFError

            end = input("Enter the end date (yyyy-mm-dd): ")
            if end == "quit":
                raise EOFError

            ratio_calculator = RatioCalculator(ticker, start, end)

            print(f"Price-to-earnings ratio: {ratio_calculator.calculate_pe_ratio()}")
        except EOFError:
            self.selector = None
            print("Exiting ratio calculator.")

    def create_plots(self):
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

            print(f"Creating plots for {tickers} from {start} to {end}")

            # Create plots here
        except EOFError:
            self.selector = None
            print("Exiting plot creator.")


if __name__ == "__main__":
    engine = Engine()
    engine.run()
