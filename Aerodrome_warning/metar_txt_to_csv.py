import csv

input_file = 'metar.txt'
output_file = 'metar_cleaned.txt'

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        line = line.strip()
        if not line or line.startswith('SA') or line.endswith('NIL='):
            continue  # Skip lines starting with 'SA', ending with 'NIL=', or empty lines
        columns = line.split()
        outfile.write(' '.join(columns) + '\n') 