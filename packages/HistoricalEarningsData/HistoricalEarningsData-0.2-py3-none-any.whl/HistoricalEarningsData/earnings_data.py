import pandas as pd
from datetime import datetime
import os

def load_earnings_data():
    """Load the earnings data from the CSV file included in the package."""
    # Get the path to the CSV file inside the installed package
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'aggregated_earnings_data_webscraped.csv')
    return pd.read_csv(file_path)

def get_earnings_dates(ticker: str, start_date: str, end_date: str, data: pd.DataFrame):
    """
    Query earnings report dates for a given stock ticker and date range.

    Parameters:
    - ticker (str): Stock ticker (e.g., 'AAPL').
    - start_date (str): Start date (format: 'YYYY-MM-DD').
    - end_date (str): End date (format: 'YYYY-MM-DD').
    - data (pd.DataFrame): DataFrame containing the earnings data.

    Returns:
    - pd.DataFrame: Filtered earnings data for the given ticker and date range.
    """
    # Parse the dates
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Convert the 'earnings_date' column to datetime for filtering
    data['earnings_date'] = pd.to_datetime(data['earnings_date'], errors='coerce')

    # Filter the data by ticker symbol and date range
    filtered_data = data[(data['symbol'] == ticker) &
                         (data['earnings_date'] >= start_date) &
                         (data['earnings_date'] <= end_date)]

    return filtered_data[['symbol', 'earnings_date', 'eps_estimate', 'reported_eps', 'surprise']]
