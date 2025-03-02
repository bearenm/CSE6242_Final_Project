import pandas as pd
import requests
import json
import time

# API Keys
NINJAS_API_KEY = "ALhKsaYwbNLR/ZGG60cyFQ==XUVxJQPFw299LKpd"


# Read the CSV files
def load_csv_data():
    constituents_df = pd.read_csv("s&p_constituents.csv")  # Date, Tickers
    sector_info_df = pd.read_csv("sector_info.csv")  # Symbol, Security, Sector, Sub-sector, etc.

    # Convert 'date' to datetime to make sorting easier
    constituents_df['date'] = pd.to_datetime(constituents_df['date'])

    return constituents_df, sector_info_df


# Function to get earnings call transcript
def get_earnings_transcript(ticker, year, quarter):
    url = f"https://api.api-ninjas.com/v1/earningstranscript?ticker={ticker}&year={year}&quarter={quarter}"
    response = requests.get(url, headers={'X-Api-Key': NINJAS_API_KEY})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching transcript for {ticker} ({year} Q{quarter}): {response.status_code}")
        print(response.json())
        return None


# Function to get the most recent S&P 500 list for a given quarter
def get_most_recent_sp500_list(constituents_df, year, quarter):
    # Original quarter's start and end dates
    start_date = pd.to_datetime(f'{year}-{(quarter - 1) * 3 + 1:02d}-01')  # Start of the quarter
    end_date = pd.to_datetime(f'{year}-{quarter * 3:02d}-01')  # End of the quarter

    # Widen the window by including the 3 months before and 3 months after the quarter
    widen_start_date = start_date - pd.DateOffset(months=3)  # 3 months before the quarter
    widen_end_date = end_date + pd.DateOffset(months=3)  # 3 months after the quarter

    # Filter the data for the widened range of dates
    filtered_df = constituents_df[
        (constituents_df['date'] >= widen_start_date) & (constituents_df['date'] < widen_end_date)]

    if filtered_df.empty:
        print(f"No data found for S&P 500 list in the widened window of {year} Q{quarter}. Skipping this quarter.")
        return pd.Series()

    most_recent_data = filtered_df.loc[filtered_df['date'].idxmax()]
    return most_recent_data


# Main function to fetch data for the last 10 years
def get_earnings_call_transcripts(output_file="earnings_transcripts.json"):
    # Initialize all_data from file if it exists, otherwise start fresh
    try:
        with open(output_file, "r") as f:
            all_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_data = {}

    constituents_df, sector_info_df = load_csv_data()

    # Trailing 10 years, iterate through Q1 - Q4
    for year in range(2025, 2026):
        for quarter in range(1, 5):
            print(f"Fetching data for {year} Q{quarter}...")

            # Get the most recent S&P 500 list for the given year and quarter
            most_recent_data = get_most_recent_sp500_list(constituents_df, year, quarter)
            if most_recent_data.empty:
                continue

            # Split tickers
            tickers = most_recent_data['tickers'].split(",")

            for ticker in tickers:
                # Remove any leading/trailing spaces
                ticker = ticker.strip()

                # Get additional reference data from sector_info_df
                sector_info = sector_info_df[sector_info_df['Symbol'] == ticker]
                if not sector_info.empty:
                    sector = sector_info['GICS Sector'].values[0]
                    industry = sector_info['GICS Sub-Industry'].values[0]
                else:
                    sector = None
                    industry = None

                print(f"Fetching transcript for ({ticker})...")
                transcript = get_earnings_transcript(ticker, year, quarter)

                if transcript:
                    # Add the fetched data
                    if year not in all_data:
                        all_data[year] = {}
                    if f"Q{quarter}" not in all_data[year]:
                        all_data[year][f"Q{quarter}"] = []

                    all_data[year][f"Q{quarter}"].append({
                        "ticker": ticker,
                        "sector": sector,
                        "industry": industry,
                        "year": year,
                        "quarter": quarter,
                        "transcript": transcript
                    })

                    # Save the data after each call to avoid loss
                    with open(output_file, "w") as f:
                        json.dump(all_data, f, indent=4)

                    print(f"Data for {ticker} saved to {output_file}")
                else:
                    print(f"Transcript not available for {ticker} ({year} Q{quarter})")

    print(f"All data saved to {output_file}")


if __name__ == "__main__":
    get_earnings_call_transcripts()