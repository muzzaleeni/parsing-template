# Web Scraping Script for 2GIS Reviews

This script performs web scraping to extract reviews from 2GIS (a popular local search service) for a given list of URLs and adds the reviews from the last 6 months to the input CSV file. Note that page is using dynamic loading.

## Prerequisites

- Python 3.6 or above is required to run the script.
- Make sure you have installed the required Python packages mentioned in the `requirements.txt`.

## Installation

1. Clone this repository to your local machine or download the script `scrape_2gis_reviews.py`.

2. Install the required Python packages by running the following command:

3. Prepare the input CSV file with the list of businesses and their 2GIS URLs. The CSV file should have the following columns:

   - `Name`: Name of the business
   - `2GIS URL`: URL of the business on 2GIS

4. Update the `input_file` and `output_file` variables in the script to point to the correct paths of your input CSV file and the output file.

5. Optionally, you can set the `new_column` variable to specify the name of the new column where the extracted reviews will be added in the CSV file.

## Usage

To run the script, use the following command in your terminal or command prompt:

The script will sequentially scrape reviews for each business URL in the input CSV file. It will add the extracted reviews to the specified new column in the CSV file.

## Notes

- The script uses Selenium with a headless browser to render JavaScript content. The headless mode can be disabled by removing the `--headless` argument from the `Options`.
- The `max_retries` variable can be adjusted to control the number of retry attempts in case of exceptions while scraping a URL.

## License

This script is licensed under the MIT License. Feel free to modify and use it according to your needs.
