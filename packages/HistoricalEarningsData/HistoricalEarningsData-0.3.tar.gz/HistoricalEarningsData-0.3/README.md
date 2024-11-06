
# HistoricalEarningsData

This Python package allows users to query historical earnings report dates for various stock tickers, now with implied volatility data on earnings dates. The dataset containing earnings and implied volatility information is bundled with the package, so no external downloads are required.

## Features

- Easily pull historical earnings data and implied volatility for popular stock tickers.
- Filter earnings data by date range.
- No need to download any datasets separately — all data is included with the package.

## Installation

You can now install this package directly from PyPI using `pip`:

```bash
pip install HistoricalEarningsData
```

## Usage Example

After installing the package, you can use the following example to query the earnings data:

```python
from HistoricalEarningsData import load_earnings_data, get_earnings_dates

# Load the earnings data from the included CSV file
data = load_earnings_data()

# Query earnings for AAPL between 2020-01-01 and 2021-12-31
earnings = get_earnings_dates("AAPL", "2020-01-01", "2021-12-31", data)

# Display results, including implied volatility on each earnings date
print(earnings[['symbol', 'earnings_date', 'eps_estimate', 'reported_eps', 'surprise', 'implied_volatility']])
```

## Dataset

The dataset used by this package includes:
- Earnings report dates, EPS estimates, reported EPS, and earnings surprises.
- Implied volatility values at the close on each earnings date, providing insight into market expectations.