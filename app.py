from flask import Flask, render_template, request
from main import get_stock_data, analyze_stock, analyze_portfolio, get_benchmark_volatility, get_risk_label

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    tickers = request.form.getlist("ticker")
    shares_list = request.form.getlist("shares")
    dates_list = request.form.getlist("purchase_date")

    results = []
    price_histories = {}  # one entry per ticker: {"dates": [...], "prices": [...]}

    for ticker, shares, purchase_date in zip(tickers, shares_list, dates_list):
        ticker = ticker.upper()
        shares = float(shares)
        data = get_stock_data(ticker, purchase_date)
        result = analyze_stock(ticker, shares, data)
        results.append(result)

        # save the price history so we can chart it later
        price_histories[ticker] = {
            "dates": data.index.strftime("%Y-%m-%d").tolist(),
            "prices": data["Close"].round(2).tolist()
        }

    summary = analyze_portfolio(results)
    earliest_date = min(dates_list)
    benchmark_volatility = get_benchmark_volatility(earliest_date)
    risk_label, risk_explanation = get_risk_label(summary["portfolio_volatility"], benchmark_volatility)

    allocation_labels = [r["ticker"] for r in results]
    allocation_values = [round(r["current_value"], 2) for r in results]

    return render_template(
        "results.html",
        results=results,
        summary=summary,
        risk_label=risk_label,
        risk_explanation=risk_explanation,
        benchmark_volatility=benchmark_volatility,
        allocation_labels=allocation_labels,
        allocation_values=allocation_values,
        price_histories=price_histories
    )

    results = []
    for ticker, shares, purchase_date in zip(tickers, shares_list, dates_list):
        ticker = ticker.upper()
        shares = float(shares)
        data = get_stock_data(ticker, purchase_date)
        result = analyze_stock(ticker, shares, data)
        results.append(result)

    summary = analyze_portfolio(results)
    earliest_date = min(dates_list)
    benchmark_volatility = get_benchmark_volatility(earliest_date)
    risk_label, risk_explanation = get_risk_label(summary["portfolio_volatility"], benchmark_volatility)

    return render_template(
        "results.html",
        results=results,
        summary=summary,
        risk_label=risk_label,
        risk_explanation=risk_explanation,
        benchmark_volatility=benchmark_volatility
    )

if __name__ == "__main__":
    app.run(debug=True)