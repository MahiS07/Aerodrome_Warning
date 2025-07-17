import pandas as pd
import re

# Read warnings
ad_warn_df = pd.read_csv('AD_warn_DF.csv')

# Read METAR lines
with open('metar_cleaned.txt', 'r') as f:
    metar_lines = [line.strip() for line in f if line.strip()]

def extract_metar_features():
    for idx, row in ad_warn_df.iterrows():
        validity_from = str(row.get('Validity from', ''))
        validity_to = str(row.get('Validity To', ''))
        print(f'\nRow {idx+1}: Validity {validity_from} to {validity_to}')
        extracting = False
        for metar in metar_lines:
            # Find the time group (e.g., 040800Z) in the METAR line
            match = re.search(r'\b(\d{6}Z)\b', metar)
            if not match:
                continue
            metar_time = match.group(1)
            if metar_time == validity_from:
                extracting = True
            if extracting:
                # Extract wind group (e.g., 28010G17KT or 28010KT)
                wind_match = re.search(r' (\d{3})(\d{2})(G(\d{2,3}))?KT', metar)
                wind_dir = int(wind_match.group(1)) if wind_match else None
                wind_gust = int(wind_match.group(4)) if wind_match and wind_match.group(4) else None
                # Extract cloud groups (e.g., SCT020 SCT025)
                clouds = re.findall(r'(FEW\d{3}|SCT\d{3}|BKN\d{3}|OVC\d{3})', metar)
                print(f'  METAR: {metar}')
                print(f'    Wind Dir: {wind_dir}, Gust: {wind_gust}, Clouds: {clouds}')
            if metar_time == validity_to and extracting:
                break

if __name__ == '__main__':
    extract_metar_features() 