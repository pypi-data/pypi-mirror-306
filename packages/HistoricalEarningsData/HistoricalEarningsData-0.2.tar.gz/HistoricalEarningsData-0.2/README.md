
    # HistoricalEarningsData

    This Python package allows users to query historical earnings report dates for various stock tickers. The dataset containing earnings information is bundled with the package, so no external downloads are required.

    ## Features

    - Easily pull historical earnings data for popular stock tickers.
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
    earnings = get_earnings_dates('AAPL', '2020-01-01', '2021-12-31', data)

    # Print the result
    print(earnings)
    ```

    ### Data Included

    The dataset included with this package contains the following columns:

    - **symbol**: The stock ticker symbol (e.g., `AAPL` for Apple).
    - **earnings_date**: The date of the earnings report.
    - **eps_estimate**: Estimated earnings per share (EPS) before the earnings report.
    - **reported_eps**: The actual reported EPS.
    - **surprise**: The difference between the estimated and actual EPS (surprise).

    The dataset is automatically loaded when you call `load_earnings_data()`.

    ### Requirements

    This package has the following dependency:
    - **pandas**: Used for handling data. This will be installed automatically with the package.

    ### License

    This project is licensed under the MIT License.
