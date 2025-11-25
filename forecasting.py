import pandas as pd
import numpy as np
import timesfm
import torch

def generate_forecast(df, months=120, model=None):
    """
    Uses Google's TimesFM model to generate a forecast for the specified number of months.
    """
    if df.empty:
        return pd.DataFrame()

    try:
        # Initialize TimesFM model if not provided
        if model is None:
            # Using the 2.5 200M parameter model as requested
            torch.set_float32_matmul_precision("high")
            try:
                model = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
            except AttributeError:
                print("Specific 2.5 class not found, trying generic TimesFM load...")
                model = timesfm.TimesFM.from_pretrained("google/timesfm-2.5-200m-pytorch")
            
            model.compile(
                timesfm.ForecastConfig(
                    max_context=1024,
                    max_horizon=months, # Set to at least the required horizon
                    normalize_inputs=True,
                    use_continuous_quantile_head=True,
                    force_flip_invariance=True,
                    infer_is_positive=True,
                    fix_quantile_crossing=True,
                )
            )

        # Prepare data
        input_data = df['CPI_YoY_Change'].values
        inputs = [input_data]

        # Generate forecast
        # The 2.5 model might expect specific args.
        # Example: model.forecast(horizon=12, inputs=...)
        
        point_forecast, quantile_forecast = model.forecast(
            inputs=inputs,
            horizon=months
        )
        
        forecast_values = point_forecast[0]
        
        # Create future dates
        last_date = df.index[-1]
        future_dates = pd.date_range(start=last_date, periods=months+1, freq='MS')[1:]
        
        # Extract quantiles for confidence intervals
        # Assuming quantile_forecast shape is (batch, horizon, quantiles)
        # We take the 10th (index 0) and 90th (index -1) percentiles
        lower_ci = quantile_forecast[0, :, 1]
        upper_ci = quantile_forecast[0, :, 9]

        forecast_df = pd.DataFrame({
            'Date': future_dates,
            'Forecast': forecast_values,
            'Lower CI': lower_ci,
            'Upper CI': upper_ci
        })
        
        forecast_df.set_index('Date', inplace=True)
        return forecast_df

    except Exception as e:
        print(f"Error generating forecast with TimesFM: {e}")
        # Fallback or re-raise
        return pd.DataFrame()

if __name__ == "__main__":
    from scraper import fetch_cpi_data
    df = fetch_cpi_data()
    if not df.empty:
        forecast = generate_forecast(df)
        print(forecast.head())
