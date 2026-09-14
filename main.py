def get_portfolio():
    """Ask the user to enter each stock they own, one at a time."""
    portfolio = []

    print("Let's build your portfolio.")
    print("Enter your stocks one at a time. Type 'done' when finished.\n")

    while True:
        ticker = input("Stock ticker (e.g. AAPL), or 'done' to finish: ").strip().upper()

        if ticker == "DONE":
            break

        shares = input(f"How many shares of {ticker} do you own? ").strip()
        purchase_date = input(f"What date did you buy {ticker}? (YYYY-MM-DD): ").strip()

        stock = {
            "ticker": ticker,
            "shares": float(shares),
            "purchase_date": purchase_date
        }
        portfolio.append(stock)

        print(f"Added {shares} shares of {ticker}, bought on {purchase_date}.\n")

    return portfolio

import yfinance as yf

from datetime import datetime

def validate_stock_input(ticker, shares, purchase_date):
    """Check the user's input before we try to analyze it. Raises ValueError with a clear message if something's wrong."""
    ticker = ticker.upper().strip()
    if not ticker:
        raise ValueError("Enter a stock ticker.")

    try:
        shares = float(shares)
    except ValueError:
        raise ValueError(f"'{shares}' is not a valid number of shares.")

    if shares <= 0:
        raise ValueError("Number of shares must be greater than zero.")

    try:
        purchase_dt = datetime.strptime(purchase_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"'{purchase_date}' is not a valid date. Use YYYY-MM-DD.")

    if purchase_dt.date() > datetime.today().date():
        raise ValueError(f"Purchase date for {ticker} can't be in the future.")

    return ticker, shares, purchase_date

def get_stock_data(ticker, purchase_date):
    """Download historical price data for a stock, starting from the purchase date."""
    stock = yf.Ticker(ticker)
    history = stock.history(start=purchase_date)

    if history.empty:
        raise ValueError(f"Couldn't find data for '{ticker}'. Check the ticker symbol.")

    return history

def analyze_stock(ticker, shares, data):
    """Calculate return, current value, and volatility for one stock."""
    purchase_price = data["Close"].iloc[0]
    current_price = data["Close"].iloc[-1]

    invested = purchase_price * shares
    current_value = current_price * shares
    gain_loss = current_value - invested
    percent_return = (gain_loss / invested) * 100

    daily_returns = data["Close"].pct_change().dropna()
    volatility = daily_returns.std() * 100

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
    benchmark = yf.Ticker("^GSPC")
    data = benchmark.history(start=start_date)
    daily_returns = data["Close"].pct_change().dropna()
    return daily_returns.std() * 100


def get_risk_label(portfolio_volatility, benchmark_volatility):
    """Convert volatility numbers into a plain-language risk description."""
    ratio = portfolio_volatility / benchmark_volatility

    if ratio < 0.8:
        return "Low", "Moves less than the overall market."
    elif ratio <= 1.2:
        return "Moderate", "Moves about the same as the overall market."
    else:
        return "High", "Moves more than the overall market."

def generate_insights(results, summary):
    """Generate short, plain-language tips based on the portfolio's numbers."""
    tips = []

    for r in results:
        weight = (r["current_value"] / summary["total_current_value"]) * 100
        if weight > 50:
            tips.append(f"{r['ticker']} is {weight:.0f}% of your portfolio. High concentration risk.")

    for r in results:
        if r["volatility"] > summary["portfolio_volatility"] * 1.3:
            tips.append(f"{r['ticker']} is more volatile than your portfolio average.")

    if len(results) > 1:
        avg_return = sum(r["percent_return"] for r in results) / len(results)
        for r in results:
            if r["percent_return"] < 0 or r["percent_return"] < avg_return - 20:
                tips.append(f"{r['ticker']} is underperforming the rest of your portfolio.")

    if len(results) < 3:
        tips.append(f"Only {len(results)} stock{'s' if len(results) != 1 else ''} held. Low diversification.")

    if not tips:
        tips.append("No major red flags.")

    return tips

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