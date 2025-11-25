import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

URL = "https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Statistics/Inflation+Data/Consumer+Prices"

def fetch_cpi_data():
    """
    Fetches CPI data from the TCMB website and returns a DataFrame.
    """
    try:
        response = requests.get(URL)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table with the specific summary attribute or by inspecting headers
        # Based on previous inspection, the table has a summary "Consumer Price Index (2003=100) (TURKSTAT)"
        table = soup.find('table', summary="Consumer Price Index (2003=100) (TURKSTAT)")
        
        if not table:
            # Fallback: try to find by header text if summary attribute changed
            headers = soup.find_all('th')
            for header in headers:
                if "CPI (Year to Year % Changes)" in header.text:
                    table = header.find_parent('table')
                    break
        
        if not table:
            raise ValueError("Could not locate the CPI data table on the page.")

        data = []
        rows = table.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                date_str = cols[0].text.strip()
                cpi_change_str = cols[1].text.strip()
                
                # Handle potential empty rows or bad formatting
                if not date_str or not cpi_change_str:
                    continue
                    
                try:
                    # Date format appears to be MM-YYYY
                    date_obj = datetime.strptime(date_str, "%m-%Y")
                    cpi_val = float(cpi_change_str)
                    data.append({"Date": date_obj, "CPI_YoY_Change": cpi_val})
                except ValueError:
                    continue

        df = pd.DataFrame(data)
        if not df.empty:
            df = df.sort_values("Date")
            df.set_index("Date", inplace=True)
            
        return df

    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    df = fetch_cpi_data()
    print(df.tail())
