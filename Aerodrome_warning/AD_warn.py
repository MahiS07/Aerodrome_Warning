import pandas as pd
import re
pd.set_option('display.max_rows', None)

with open("AERODROM WARNING COMPOSITE 0F SEPTEMBER 2023.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

data = []
i = 0
while i < len(lines):
    
    if "WARNING" in lines[i] :
        i += 2
        if i >= len(lines): break
        
        
        main_line = lines[i]
        main_parts = main_line.split()
        station = main_parts[0]
        issue_time = main_parts[1]
        validity_from, validity_to = "", ""
        valid_match = re.search(r"VALID\s*(\d{6,8})/(\d{6,8})", main_line)
        if valid_match:
            validity_from = f"{valid_match.group(1)}Z"
            validity_to = f"{valid_match.group(2)}Z"
        
        
        i += 1
        if i >= len(lines): break
        wx_line = lines[i]
        wind_dir, wind_speed, gust, sig_wx, fcst_obs = "", "", "", "", ""
        
        
        wind_speed_match = re.search(r"SFC WSPD (\d+KT)", wx_line)
        wind_speed = wind_speed_match.group(1) if wind_speed_match else ""
        
        gust_match = re.search(r"MAX(\d+)", wx_line)
        gust = f"{gust_match.group(1)}KT" if gust_match else ""
        
        
        wind_dir_dict = {
            "N": 0,
            "NNE": 20,
            "NE": 50,
            "ENE": 70,
            "E": 90,
            "ESE": 110,
            "SE": 140,
            "SSE": 160,
            "S": 180,
            "SSW": 200,
            "SW": 230,
            "WSW": 250,
            "W": 270,
            "WNW": 290,
            "NW": 320,
            "NNW": 340
        }
        wind_dir_match = re.search(r"FROM\s+([A-Z]+)", wx_line)
        if wind_dir_match:
            wind_dir_str = wind_dir_match.group(1).strip()
            wind_dir = wind_dir_str
            wind_dir_num = wind_dir_dict.get(wind_dir_str, "")
        else:
            wind_dir = ""
            wind_dir_num = ""
        
        sig_wx_match = re.search(r"(TSRA|TS|FBL TSRA|MOD TSRA|HVY TSRA|MOD TS|FBL TS|HVY TS)", wx_line)
        sig_wx = sig_wx_match.group(1) if sig_wx_match else ""
        if "HVY TSRA" in wx_line:
            sig_wx = "+TSRA"
        elif "FBL TSRA" in wx_line:
            sig_wx = "-TSRA"
        elif "MOD TSRA" in wx_line or "TSRA" in wx_line:
            sig_wx = "TSRA"
        elif "HVY TS" in wx_line:
            sig_wx = "+TS"
        elif "FBL TS" in wx_line:
            sig_wx = "-TS"
        elif "MOD TS" in wx_line or "TS" in wx_line:
            sig_wx = "TS"
        else:
            sig_wx = ""
        
        
        if "FCST" in wx_line:
            fcst_obs = "FCST"
        elif "OBS" in wx_line or "OBSD" in wx_line:
            fcst_obs = "OBS"
        
        data.append({
            "Station": station,
            "Issue date/time": issue_time,
            "Validity from": validity_from,
            "Validity To": validity_to,
            "Wind dir (deg)": wind_dir_num,
            "Wind Speed": wind_speed,
            "Gust": gust,
            "Significant Wx": sig_wx,
            "FCST/OBS": fcst_obs
        })
    i += 1


df = pd.DataFrame(data)

df["Wind dir (deg)"] = pd.to_numeric(df["Wind dir (deg)"], errors="coerce").astype("Int64")
print(df)
df.to_csv('AD_warn_DF.csv')