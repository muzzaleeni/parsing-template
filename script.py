import csv
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import locale, re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the input file path
input_file = "/Users/muzzyaqow/Desktop/updated-database.csv"
output_file = (
    "/Users/muzzyaqow/Documents/projects/Gourmenta/server/updated-database.csv"
)

# Set the new column name
new_column = "Reviews"

# Set the maximum number of retries
max_retries = 3

# Set the Russian locale for date parsing
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")


# Function to extract the date from the text with possible additional text
def extract_date(text):
    # Regular expression to match the date part (e.g., '23 июля 2023')
    date_pattern = re.compile(r"\d{1,2}\s\w+\s\d{4}")
    # Find the date part in the text
    match = date_pattern.search(text)
    if match:
        return match.group()
    else:
        return None


# Function to parse the date text, handling "сегодня" case
def parse_date(date_text):
    if "сегодня" in date_text:
        # Replace "сегодня" with the current date
        today = datetime.today()
        date_text = date_text.replace("сегодня", today.strftime("%d %B %Y"))
    return date_text


def wait_for_element(driver, by, selector, timeout=1):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, selector))
        )
    except Exception as e:
        return None  # Re-raise the exception to propagate it further


def scrape_reviews(row, row_num):
    url = (
        row.get("2GIS URL") + "/tab/reviews"
    )  # Use .get() to handle missing key gracefully
    if not url:
        print(f"Missing '2GIS URL' in row: {row_num}")
        return None

    # Set up Selenium with a headless browser
    options = Options()
    options.add_argument(
        "--non-headless"
    )  # Run the browser in headless mode (optional)
    options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)
    driver = webdriver.Chrome(
        options=options
    )  # Change this to the path of your web driver

    retries = 0
    reviews = []
    last_parsed_date = None  # Keep track of the last parsed date for the row

    while retries < max_retries:
        try:
            driver.get(url)

            while True:
                # Continue with the rest of the code (parsing reviews and dates)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                review_elements = soup.find_all("div", class_="_11gvyqv")
                today = datetime.today().replace(
                    hour=0, minute=0, second=0, microsecond=0
                )

                new_reviews_count = (
                    0  # Count the number of new reviews loaded in this scroll
                )
                for review_element in review_elements:
                    # Extract review body from the <a> tag
                    review_body = review_element.find("a").text.strip()

                    # Find the date element and extract the date text
                    date_element = review_element.find("div", class_="_4mwq3d")
                    date_text = date_element.text.strip()

                    # Remove the additional text ", отредактирован" if present
                    date_text = date_text.split(",")[0]

                    # Parse the date text, handling "сегодня" case
                    date_text = parse_date(date_text)

                    # Parse the date using a known format
                    review_date = datetime.strptime(
                        extract_date(date_text), "%d %B %Y"
                    ).replace(hour=0, minute=0, second=0, microsecond=0)

                    # Check if the review is within the last 3 months
                    if (today - review_date) <= timedelta(days=180):
                        # Increment the review counter
                        new_reviews_count += 1

                        # Format the review with the review number
                        formatted_review = f"Review {new_reviews_count}: {review_body}"
                        reviews.append(formatted_review)

                        # Update the last parsed date for the row
                        last_parsed_date = review_date
                    else:
                        new_reviews_count = 0
                        break

                # Check if the "Load more" button is present and wait for it to be visible
                try:
                    load_more_button = wait_for_element(
                        driver, By.XPATH, "//button[contains(text(), 'Загрузить ещё')]"
                    )
                except Exception as e:
                    break

                if load_more_button is None or not load_more_button.is_displayed():
                    break

                # If all new reviews loaded in this scroll are older than 90 days, break from the loop
                if new_reviews_count == 0:
                    break

                driver.execute_script(
                    "arguments[0].scrollIntoView();", load_more_button
                )
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(0.5)
                load_more_button = wait_for_element(
                    driver, By.XPATH, "//button[contains(text(), 'Загрузить ещё')]"
                )

            row[new_column] = "\n".join(reviews)
            # Check if last_parsed_date is not None before formatting it
            if last_parsed_date is not None:
                print(
                    f"Row Number: {row_num}, Name: {row.get('Name')}, Last Parsed Date: {last_parsed_date.strftime('%Y-%m-%d')}"
                )

            driver.quit()  # Close the browser after scraping reviews

            return row
        except Exception as e:
            print(f"Exception occurred: {e}")
            driver.quit()  # Close the browser if an exception occurs
            retries += 1
            time.sleep(1)

    print(f"Max retries reached for Row Number: {row_num}")
    return None


# Scrape reviews sequentially for each row
updated_rows = []
with open(input_file, "r", newline="") as file_in:
    reader = csv.DictReader(file_in)
    fieldnames = reader.fieldnames + [new_column]

    for row_num, row in enumerate(reader, start=1):
        updated_row = scrape_reviews(row, row_num)
        if updated_row is not None:
            updated_rows.append(updated_row)

# Update the existing CSV file with the modified rows
with open(output_file, "w", newline="") as file_out:
    writer = csv.DictWriter(file_out, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print("Reviews from the last 6 months have been added to the input CSV file.")
