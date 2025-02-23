from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time

 
def scrape_data( name_file, website_link, post_limit):

    # Initialize WebDriver with headless option
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())  # Automatically downloads the correct ChromeDriver
    driver = webdriver.Chrome(service=service)

    driver.get(website_link)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    job_listings = driver.find_elements(By.XPATH, '//*[@id="main-content"]/section[2]/ul/li')

    # Open the CSV file for writing
    with open( 'scrapped_data/'+name_file+'.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Company", "Date", "Address", "Link", "Description"])

        count = 0
        for listing in job_listings:
            if count >= post_limit:  # Limit to job postings
                break

            job_title_element = listing.find_element(By.CLASS_NAME, 'base-search-card__title')
            job_title = job_title_element.text
            print("Job title :", job_title)

            company_element = listing.find_element(By.CLASS_NAME, 'base-search-card__subtitle')
            company = company_element.text
            print("Company :", company)
            # if company.strip() == "Epic":  # Skip Epic Jobs
            #     continue
        
            address_element = listing.find_element(By.CLASS_NAME, 'job-search-card__location')
            address = address_element.text
            print("Address :", address)

            date_element = listing.find_element(By.XPATH, '//*[starts-with(@class, "job-search-card__listdate")]')
            date = date_element.text
            print("Date :", date)
        
            link_element = listing.find_element(By.CLASS_NAME,'base-card__full-link')
            job_link = link_element.get_attribute('href')
            print("Link :", job_link)
        
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(job_link)
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

            job_description = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]')
            description_element = job_description.find_element(By.XPATH, '//*[@class="description__text description__text--rich"]')
            description_html = description_element.get_attribute('innerHTML')
        
            # Use BeautifulSoup to prettify the HTML content
            soup = BeautifulSoup(description_html, 'html.parser')
            pretty_html = soup.prettify()
            print("Description (HTML format):", pretty_html)
            
            print("-"*50)

            # Write the job details to the CSV file
            writer.writerow([job_title, company, date, address, job_link, pretty_html])
            count += 1
            
    # Close the browser
    driver.quit()
