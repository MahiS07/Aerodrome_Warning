import os
import csv
import re

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'metar.txt')
output_file = os.path.join(script_dir, 'metar.csv')

def parse_metar_line(line):
    """
    Parse a METAR line and extract the timestamp and METAR string.
    Returns (timestamp, metar_report) or (None, None) if not matched.
    """
    # Example: METAR VABB 040800Z 28010KT 3000 HZ SCT020 SCT025 31/25 Q1006 NOSIG=
    match = re.match(r"METAR (VABB) (\d{6}Z) (.+)", line)
    if match:
        station = match.group(1)
        datetime = match.group(2)
        report = match.group(3)
        return station, datetime, report
    return None, None, None

def main():
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        # Write header
        writer.writerow(['station', 'datetime', 'report'])
        for line in infile:
            line = line.strip()
            if line.startswith('SA'):
                continue  # Skip 'SA' lines
            if line.startswith('METAR'):
                station, datetime, report = parse_metar_line(line)
                if station and datetime and report:
                    writer.writerow([station, datetime, report])

if __name__ == '__main__':
    main() 