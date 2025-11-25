import argparse
import datetime
import os
import pandas as pd
from scraper import fetch_cpi_data
from forecasting import generate_forecast

DATA_DIR = "data"
LATEST_CPI_FILE = os.path.join(DATA_DIR, "latest_cpi.csv")
FORECAST_FILE = os.path.join(DATA_DIR, "forecast.csv")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def run_update():
    print(f"[{datetime.datetime.now()}] Starting scheduled update...")
    
    try:
        # 1. Fetch Data
        print("Fetching CPI data...")
        df = fetch_cpi_data()
        if df.empty:
            print("Error: Fetched data is empty.")
            return

        ensure_data_dir()
        df.to_csv(LATEST_CPI_FILE)
        print(f"Saved CPI data to {LATEST_CPI_FILE}")

        # 2. Generate Forecast
        print("Generating forecast...")
        forecast_df = generate_forecast(df)
        
        if not forecast_df.empty:
            forecast_df.to_csv(FORECAST_FILE)
            print(f"Saved forecast to {FORECAST_FILE}")
        else:
            print("Error: Forecast generation failed.")

        print("Update completed successfully.")

    except Exception as e:
        print(f"An error occurred during the update: {e}")

def main():
    parser = argparse.ArgumentParser(description="CPI Forecast Scheduler")
    parser.add_argument("--force", action="store_true", help="Force run the update regardless of the date")
    args = parser.parse_args()

    today = datetime.date.today()
    
    if args.force:
        print("Force flag detected. Running update...")
        run_update()
    elif today.day == 30:
        print("It is the 30th of the month. Running update...")
        run_update()
    else:
        print(f"Today is {today}. Skipping update (runs only on the 30th). Use --force to override.")

if __name__ == "__main__":
    main()
