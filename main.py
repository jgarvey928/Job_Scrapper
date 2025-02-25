from scrape_data import scrape_data
from extract_data import extract_data
from analyze_data import analyze_data
from generate_letters import generate_letters
import time

if __name__ == '__main__':

    # # Software Engineer - United States - Entry Level - Remote - Past Month
    # website_link = "https://www.linkedin.com/jobs/search/?currentJobId=4137506459&f_E=2&f_TPR=r2592000&f_WT=2&geoId=103644278&keywords=software%20engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"
    # name_files = "se_us_entry_remote_month_02_24_25"

    # Software Engineer - Greater Phoenix - Entry Level - Hybrid / Onsite - Past Month
    website_link = "https://www.linkedin.com/jobs/search/?currentJobId=4132363569&f_E=2&f_TPR=r2592000&f_WT=1%2C3&geoId=90000620&keywords=software%20engineer&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true"
    name_files = "se_phx_entry_onsite_month_02_24_25"
    
    # # # Data Analyst - Greater Phoenix - Entry Level - Hybrid / Onsite - Past Month
    # website_link = "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Greater%20Phoenix%20Area&geoId=90000620&f_JT=F&f_E=2&f_TPR=r2592000&f_WT=1%2C3&position=1&pageNum=0"
    # name_files = "da_phx_entry_onsite_month_02_24_25"

    # # # Data Engineer - United States - Entry Level - Remote - Past Month
    # website_link = "https://www.linkedin.com/jobs/search?keywords=Data%20Engineer&location=United%20States&geoId=103644278&f_JT=F&f_E=2&f_TPR=&f_WT=2&position=1&pageNum=0"
    # name_files = "de_us_entry_remote_month_02_24_25_2"

    scrape_data(name_files, website_link, 80)
    
    # Wait for n seconds
    time.sleep(5)
    
    extract_data(name_files)
    analyze_data(name_files)
    generate_letters(name_files, 4)

    #TODO: Choose which top jobs to generate letters for
    #TODO: Fine tune requirements collection keywords in extract_data.py
    #TODO: Try to collect more than 60 job postings
    #TODO: Collect from multiple locations
    #TODO: Add gradle build for run with passing link and file name
    #TODO: Containerize the project
    #TODO: Update README.md and add author / date / description