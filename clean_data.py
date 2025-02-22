import csv
from bs4 import BeautifulSoup

def clean_html(description):
    soup = BeautifulSoup(description, 'html.parser')
    text = soup.get_text(separator="\n")
    # Remove leading/trailing whitespaces and empty lines
    cleaned_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
    return cleaned_text

def clean_csv(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in reader:
            row['Description'] = clean_html(row['Description'])
            writer.writerow(row)

# Define input and output file names
input_csv = 'job_listings5.csv'
output_csv = 'cleaned_job_listings3.csv'

# Clean the CSV file
clean_csv(input_csv, output_csv)

print(f"Cleaned CSV saved as {output_csv}")
