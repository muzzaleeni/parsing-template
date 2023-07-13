import csv
import time
import requests
from bs4 import BeautifulSoup
import sys

# Set the input file path
input_file = "results.csv"

# Set the new column name
new_column = "Доп. информация"

# Set the maximum number of retries
max_retries = 3


# Function to scrape additional information from the webpage
def scrape_additional_info(args):
    row, row_num = args
    url = row["2GIS URL"] + "/tab/info"
    retries = 0

    while retries < max_retries:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
            }

            response = requests.get(url, headers=headers, verify=True, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")

            span_elements = soup.find_all("span", class_="_er2xx9")
            info = [span.text.strip() for span in span_elements]

            info_text = " ".join(info)

            row[new_column] = info_text

            print(f"Row Number: {row_num}, Name: {row['Наименование']}")
            sys.stdout.flush()

            return row
        except Exception as e:
            print(f"Exception occurred: {e}")
            print("Retrying...")
            sys.stdout.flush()
            retries += 1
            time.sleep(5)

    print(f"Max retries reached for Row Number: {row_num}")
    sys.stdout.flush()
    return None


# Read the input CSV file
rows = []
with open(input_file, "r", newline="") as file_in:
    reader = csv.DictReader(file_in)
    fieldnames = reader.fieldnames + [new_column]

    for row_num, row in enumerate(reader, start=1):
        rows.append((row, row_num))

# Scrape additional information
updated_rows = []
for i, row in enumerate(rows, start=1):
    updated_row = scrape_additional_info(row)
    if updated_row is not None:
        updated_rows.append(updated_row)

# Update the existing CSV file with the modified rows
with open(input_file, "w", newline="") as file_out:
    writer = csv.DictWriter(file_out, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print("Additional information has been added to the input CSV file.")
