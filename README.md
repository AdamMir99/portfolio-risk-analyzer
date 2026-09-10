# Portfolio Risk Analyzer

A Python command-line tool that analyzes a stock portfolio's performance and risk, using real historical market data. Built as a personal project to apply concepts from financial analysis and risk management in code.

## What it does

- Lets a user manually enter the stocks they own (ticker, number of shares, purchase date)
- Pulls real historical price data for each stock using [yfinance](https://pypi.org/project/yfinance/)
- Calculates key metrics for each stock and for the portfolio as a whole:
  - Return (gain/loss in dollars and %)
  - Volatility (how much the price swings day to day)
  - Portfolio-wide volatility, weighted by position size
- Compares the portfolio's volatility against the S&P 500 to show relative risk
- Presents results in two layers:
  - **At a glance** — a simple, plain-language summary (current value, return, risk level)
  - **Details** — a full breakdown of the underlying numbers, for anyone who wants to dig deeper

## Why I built this

I'm a first-year student at the University of Waterloo studying financial analysis and risk management. I wanted a hands-on project that combined what I'm learning in class with real coding skills, and that I could point to on my resume/LinkedIn for co-op applications.

## Tech stack

- **Python**
- **yfinance** — historical stock price data
- **pandas / numpy** — data handling and calculations
- **matplotlib** — (planned) visualizations

## How to run it

1. Clone this repo:
   git clone https://github.com/AdamMir99/portfolio-risk-analyzer.git

2. Install the required libraries:
3. Run the program:
4. Follow the prompts to enter your stocks (ticker, shares, purchase date). Type `done` when finished.

## Example output
========================================
YOUR PORTFOLIO, AT A GLANCE

Value: $8040.41 (+2113.83% since purchase)
Risk level: High
Your portfolio moves more than the overall market — bigger swings up and down.

========================================
DETAILS

Total invested: $363.19
Total gain/loss: $7677.22
Portfolio volatility: 2.47%
S&P 500 volatility (same period): 1.25%

Per-stock breakdown:
AAPL: $20.35 -> $1295.00 (6263.85%), volatility 1.91%
NVDA: $1.77 -> $874.08 (49408.82%), volatility 3.06%
META: $341.07 -> $5871.33 (1621.42%), volatility 2.51%


## Planned improvements

- [ ] Price charts with buy/sell dates marked
- [ ] Value at Risk (VaR) calculation
- [ ] Correlation between holdings (diversification check)
- [ ] Input validation / error handling for invalid tickers or dates

## Status

Actively in development as a learning project.
