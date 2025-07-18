import pandas as pd
import re

# Read warnings
ad_warn_df = pd.read_csv('AD_warn_DF.csv')

# Read METAR lines
with open('metar.txt', 'r') as f:
    metar_lines = [line.strip() for line in f if line.strip()]

def get_metar_time_group(metar):
    # Try to extract the Z group (e.g., 231105Z)
    match = re.search(r'\b(\d{6}Z)\b', metar)
    if match:
        return match.group(1)[:-1]  # Remove 'Z'
    # If not found, try to extract the full timestamp and round minutes down to zero
    match_full = re.match(r'(\d{8})(\d{4})', metar)
    if match_full:
        date_part = match_full.group(1)  # YYYYMMDD
        time_part = match_full.group(2)  # HHMM
        hour = time_part[:2]
        # Round minutes down to zero
        rounded_time = f"{date_part}{hour}00"
        # Return last 6 digits (no 'Z')
        return rounded_time[-6:]
    return None

def extract_metar_features():
    with open('metar_extracted_features.txt', 'w') as out:
        for idx, row in enumerate(ad_warn_df.iterrows()):
            fcst_obs = str(row[1].get('FCST/OBS', '')).strip().upper()
            if fcst_obs != 'FCST':
                out.write(f'\nRow {idx+1}: FCST/OBS is {fcst_obs}, skipping extraction.\n')
                continue
            validity_from = str(row[1].get('Validity from', '')).replace('Z', '')
            validity_to = str(row[1].get('Validity To', '')).replace('Z', '')
            out.write(f'\nRow {idx+1}: Validity {validity_from} to {validity_to}\n')
            extracting = False
            for metar in metar_lines:
                metar_time = get_metar_time_group(metar)
                if not metar_time:
                    continue
                if metar_time == validity_from:
                    extracting = True
                if extracting:
                    # Extract wind group (e.g., 28010G17KT or 28010KT)
                    wind_match = re.search(r' (\d{3})(\d{2})(G(\d{2,3}))?KT', metar)
                    wind_dir = int(wind_match.group(1)) if wind_match else None
                    wind_gust = int(wind_match.group(4)) if wind_match and wind_match.group(4) else None
                    # Extract cloud groups (e.g., SCT020 SCT025, FEW030CB)
                    clouds = re.findall(r'(FEW\d{3}(?:CB|TCU)?|SCT\d{3}(?:CB|TCU)?|BKN\d{3}(?:CB|TCU)?|OVC\d{3}(?:CB|TCU)?)', metar)
                    out.write(f'  METAR: {metar}\n')
                    out.write(f'    Wind Dir: {wind_dir}, Gust: {wind_gust}, Clouds: {clouds}\n')
                if metar_time == validity_to and extracting:
                    break

if __name__ == '__main__':
    extract_metar_features() 