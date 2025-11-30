# Turkey CPI Forecast App 🇹🇷

This application scrapes the latest **Consumer Price Index (Year to Year % Changes)** data from the [Central Bank of the Republic of Türkiye (TCMB)](https://www.tcmb.gov.tr/) and forecasts the trend for the next 10 years (120 months) using Google's **TimesFM** model.

## Features

-   **Automated Scraping**: Fetches the latest CPI data directly from the TCMB website.
-   **Advanced Forecasting**: Uses the TimesFM (Time Series Foundation Model) 2.5 200M model for accurate long-term predictions.
-   **Interactive Visualization**: Displays historical and forecasted data with confidence intervals using Plotly.
-   **Automated Updates**: Includes a scheduler to automatically update data and forecasts on the 30th of every month.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/ggaammdev/cpi_estimate
    cd cpi_estimate
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Web App

Start the Streamlit application:

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`.

### Manual Update

To run the data scraping and forecasting process immediately (bypassing the schedule check):

```bash
python scheduler.py --force
```

### Setting up the Scheduler

To enable automatic monthly updates (runs on the 30th):

1.  Run the setup helper:
    ```bash
    ./setup_cron.sh
    ```
2.  Follow the on-screen instructions to add the cron job to your system.

## Project Structure

-   `app.py`: Main Streamlit application.
-   `scraper.py`: Logic for scraping data from TCMB.
-   `forecasting.py`: Logic for generating forecasts using TimesFM.
-   `scheduler.py`: Script for the automated update process.
-   `run_scheduler.sh`: Wrapper script for the cron job.
-   `data/`: Directory storing the CSV data files.

## License

Apache License 2.0
