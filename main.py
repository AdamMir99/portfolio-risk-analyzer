# Portfolio Risk Analyzer
# Step 1: Collect the user's portfolio (stocks, shares, purchase date)

def get_portfolio():
    """Ask the user to enter each stock they own, one at a time."""
    portfolio = []  # this will hold a list of stocks the user enters

    print("Let's build your portfolio.")
    print("Enter your stocks one at a time. Type 'done' when finished.\n")

    while True:
        ticker = input("Stock ticker (e.g. AAPL), or 'done' to finish: ").strip().upper()

        if ticker == "DONE":
            break

        shares = input(f"How many shares of {ticker} do you own? ").strip()
        purchase_date = input(f"What date did you buy {ticker}? (YYYY-MM-DD): ").strip()

        # save this stock's info as a dictionary
        stock = {
            "ticker": ticker,
            "shares": float(shares),
            "purchase_date": purchase_date
        }
        portfolio.append(stock)

        print(f"Added {shares} shares of {ticker}, bought on {purchase_date}.\n")

    return portfolio

import yfinance as yf

def get_stock_data(ticker, purchase_date):
    """Download historical price data for a stock, starting from the purchase date."""
    stock = yf.Ticker(ticker)
    history = stock.history(start=purchase_date)  # prices from purchase date to today
    return history

def analyze_stock(ticker, shares, data):
    """Calculate return, current value, and volatility for one stock."""
    purchase_price = data["Close"].iloc[0]   # first closing price after purchase date
    current_price = data["Close"].iloc[-1]   # most recent closing price

    invested = purchase_price * shares
    current_value = current_price * shares
    gain_loss = current_value - invested
    percent_return = (gain_loss / invested) * 100

    daily_returns = data["Close"].pct_change().dropna()  # day-to-day % change
    volatility = daily_returns.std() * 100  # how much the price swings, on average

    return {
        "ticker": ticker,
        "purchase_price": purchase_price,
        "current_price": current_price,
        "invested": invested,
        "current_value": current_value,
        "gain_loss": gain_loss,
        "percent_return": percent_return,
        "volatility": volatility
    }

def analyze_portfolio(results):
    """Combine individual stock results into one overall portfolio summary."""
    total_invested = sum(r["invested"] for r in results)
    total_current_value = sum(r["current_value"] for r in results)
    total_gain_loss = total_current_value - total_invested
    total_percent_return = (total_gain_loss / total_invested) * 100

    # weighted average volatility, based on how much money is in each stock
    weighted_volatility = sum(
        r["volatility"] * (r["current_value"] / total_current_value) for r in results
    )

    return {
        "total_invested": total_invested,
        "total_current_value": total_current_value,
        "total_gain_loss": total_gain_loss,
        "total_percent_return": total_percent_return,
        "portfolio_volatility": weighted_volatility
    }

def get_benchmark_volatility(start_date):
    """Get the S&P 500's volatility over the same period, for comparison."""
    benchmark = yf.Ticker("^GSPC")  # ^GSPC is the ticker symbol for the S&P 500
    data = benchmark.history(start=start_date)
    daily_returns = data["Close"].pct_change().dropna()
    return daily_returns.std() * 100


def get_risk_label(portfolio_volatility, benchmark_volatility):
    """Convert volatility numbers into a plain-language risk description."""
    ratio = portfolio_volatility / benchmark_volatility

    if ratio < 0.8:
        return "Low", "Your portfolio moves less than the overall market — generally calmer, more stable."
    elif ratio <= 1.2:
        return "Moderate", "Your portfolio moves about as much as the overall market."
    else:
        return "High", "Your portfolio moves more than the overall market — bigger swings up and down."

if __name__ == "__main__":
    my_portfolio = get_portfolio()

    print("\nFetching price history and analyzing...\n")
    results = []
    for stock in my_portfolio:
        data = get_stock_data(stock["ticker"], stock["purchase_date"])
        result = analyze_stock(stock["ticker"], stock["shares"], data)
        results.append(result)

        print(f"--- {result['ticker']} ---")
        print(f"Invested: ${result['invested']:.2f}")
        print(f"Current value: ${result['current_value']:.2f}")
        print(f"Gain/Loss: ${result['gain_loss']:.2f} ({result['percent_return']:.2f}%)")
        print(f"Daily volatility: {result['volatility']:.2f}%")
        print()

        summary = analyze_portfolio(results)

     # use the earliest purchase date across the portfolio for a fair benchmark comparison
    earliest_date = min(stock["purchase_date"] for stock in my_portfolio)
    benchmark_volatility = get_benchmark_volatility(earliest_date)
    risk_label, risk_explanation = get_risk_label(summary["portfolio_volatility"], benchmark_volatility)

    print("=" * 40)
    print("YOUR PORTFOLIO, AT A GLANCE")
    print("=" * 40)
    print(f"Value: ${summary['total_current_value']:.2f} "
          f"({'+' if summary['total_gain_loss'] >= 0 else ''}{summary['total_percent_return']:.2f}% since purchase)")
    print(f"Risk level: {risk_label}")
    print(risk_explanation)

    print("\n" + "=" * 40)
    print("DETAILS")
    print("=" * 40)
    print(f"Total invested: ${summary['total_invested']:.2f}")
    print(f"Total gain/loss: ${summary['total_gain_loss']:.2f}")
    print(f"Portfolio volatility: {summary['portfolio_volatility']:.2f}%")
    print(f"S&P 500 volatility (same period): {benchmark_volatility:.2f}%")
    print("\nPer-stock breakdown:")
    for r in results:
        print(f"  {r['ticker']}: ${r['invested']:.2f} -> ${r['current_value']:.2f} "
              f"({r['percent_return']:.2f}%), volatility {r['volatility']:.2f}%")