# Web Scraping Additional Information from 2GIS

This script allows you to scrape additional information from webpages using the 2GIS website. It takes an input CSV file containing URLs and adds a new column with the scraped information to the file.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `csv` library

## Installation

1. Make sure you have Python 3.x installed on your system.
2. Install the required libraries by running the following command:

`pip install requests beautifulsoup4`


## Usage

1. Prepare your input CSV file (`results.csv`) with a column named `2GIS URL` containing the URLs of the webpages you want to scrape additional information from.
2. Place the script (`script.py`) in the same directory as your input CSV file.
3. Open a terminal or command prompt and navigate to the directory containing the script.
4. Run the script by executing the following command:

`python script.py`


5. The script will start scraping the additional information from the webpages. It will print the row number and name of each processed restaurant to track the progress.
6. Once the script finishes, it will update the input CSV file (`results.csv`) with the scraped information. The additional information will be stored in a new column named `Доп. информация`.
7. You can check the updated CSV file to see the added information.

## Configuration

- `input_file`: Set the path of your input CSV file (default: "results.csv").
- `new_column`: Set the name of the new column to store the scraped information (default: "Доп. информация").
- `max_retries`: Set the maximum number of retries for failed requests (default: 3).

## Notes

- The script handles common exceptions that may occur during the request and retries the failed requests up to the specified number of retries.
- The script uses a user-agent header to mimic Chrome on macOS for better compatibility with websites.
- Make sure to respect the website's terms of service and the legal aspects
