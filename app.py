import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scraper import fetch_cpi_data
from forecasting import generate_forecast

st.set_page_config(page_title="CPI Forecast App", layout="wide")

st.title("🇹🇷 Turkey CPI Forecast App")
st.markdown("""
This application scrapes the latest **Consumer Price Index (Year to Year % Changes)** data from the 
[Central Bank of the Republic of Türkiye (TCMB)](https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Statistics/Inflation+Data/Consumer+Prices) 
and forecasts the trend for the next 10 years (120 months).
""")

import os

DATA_DIR = "data"
LATEST_CPI_FILE = os.path.join(DATA_DIR, "latest_cpi.csv")
FORECAST_FILE = os.path.join(DATA_DIR, "forecast.csv")

@st.cache_data(ttl=3600)
def load_data():
    if os.path.exists(LATEST_CPI_FILE):
        try:
            df = pd.read_csv(LATEST_CPI_FILE, parse_dates=['Date'], index_col='Date')
            return df, "Cached"
        except Exception as e:
            st.warning(f"Failed to load cached data: {e}")
    
    return fetch_cpi_data(), "Live"

@st.cache_resource
def load_model():
    # Initialize TimesFM model
    # Using the 2.5 200M parameter model
    import timesfm
    import torch
    torch.set_float32_matmul_precision("high")
    try:
        model = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
    except AttributeError:
        model = timesfm.TimesFM.from_pretrained("google/timesfm-2.5-200m-pytorch")
    
    model.compile(
        timesfm.ForecastConfig(
            max_context=1024,
            max_horizon=120, # Fixed horizon for the app
            normalize_inputs=True,
            use_continuous_quantile_head=True,
            force_flip_invariance=True,
            infer_is_positive=True,
            fix_quantile_crossing=True,
        )
    )
    return model

with st.spinner("Loading data..."):
    df, source = load_data()

if df.empty:
    st.error("Failed to fetch data. Please check the data source or try again later.")
else:
    # Display latest data
    latest_date = df.index[-1]
    latest_value = df['CPI_YoY_Change'].iloc[-1]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Latest Date", latest_date.strftime("%B %Y"))
    col2.metric("Latest CPI (YoY %)", f"{latest_value:.2f}%")
    col3.info(f"Data Source: {source}")
    
    # Generate Forecast
    forecast_df = pd.DataFrame()
    
    if source == "Cached" and os.path.exists(FORECAST_FILE):
        try:
            forecast_df = pd.read_csv(FORECAST_FILE, parse_dates=['Date'], index_col='Date')
        except Exception as e:
            st.warning(f"Failed to load cached forecast: {e}")
            
    if forecast_df.empty:
        with st.spinner("Generating forecast (Live)..."):
            model = load_model()
            forecast_df = generate_forecast(df, months=120, model=model)

    # Visualization
    fig = go.Figure()

    # Historical Data
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['CPI_YoY_Change'],
        mode='lines+markers',
        name='Historical CPI',
        line=dict(color='blue')
    ))

    if not forecast_df.empty:
        # Forecast Data
        fig.add_trace(go.Scatter(
            x=forecast_df.index,
            y=forecast_df['Forecast'],
            mode='lines',
            name='Forecast',
            line=dict(color='red', dash='dash')
        ))
        
        # Confidence Interval
        fig.add_trace(go.Scatter(
            x=list(forecast_df.index) + list(forecast_df.index[::-1]),
            y=list(forecast_df['Upper CI']) + list(forecast_df['Lower CI'][::-1]),
            fill='toself',
            fillcolor='rgba(255, 0, 0, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=True,
            name='Confidence Interval'
        ))

    fig.update_layout(
        title="CPI (Year to Year % Changes) - Historical & Forecast",
        xaxis_title="Date",
        yaxis_title="CPI % Change",
        hovermode="x unified",
        template="plotly_white"
    )

    st.plotly_chart(fig, width='stretch')

    # Data Table
    with st.expander("View Raw Data"):
        col_hist, col_pred = st.columns(2)
        
        with col_hist:
            st.subheader("Historical Data")
            st.dataframe(df.sort_index(ascending=False))
            
        with col_pred:
            st.subheader("Forecast Data")
            st.dataframe(forecast_df)

    st.markdown("---")
    st.caption("Data Source: Central Bank of the Republic of Türkiye")
