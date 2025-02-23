from scrape_data import scrape_data
from extract_data import extract_data
from analyze_data import analyze_data
import time

if __name__ == '__main__':

    # # Software Engineer - United States - Entry Level - Remote - Past Month
    # website_link = "https://www.linkedin.com/jobs/search/?currentJobId=4137506459&f_E=2&f_TPR=r2592000&f_WT=2&geoId=103644278&keywords=software%20engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"
    # name_files = "se_us_entry_remote_month_02_23_25"

    # Software Engineer - Greater Phoenix - Entry Level - Hybrid / Onsite - Past Month
    website_link = "https://www.linkedin.com/jobs/search/?currentJobId=4132363569&f_E=2&f_TPR=r2592000&f_WT=1%2C3&geoId=90000620&keywords=software%20engineer&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true"
    name_files = "se_phx_entry_onsite_month_02_23_25"
    
    scrape_data(name_files, website_link, 80)
    
    # Wait for n seconds
    time.sleep(5)
    
    extract_data(name_files)
    analyze_data(name_files)

    #TODO: Fine tune requirements collection in extract_data.py
    #TODO: Try to collect more than 60 job postings
    #TODO: Collect from multiple locations
    #TODO: Try Data Engineer, Data Analyst, Data Scientist, etc.
    #TODO: Auto complete CV for Junior, Entry-Level, I, Early-Career, etc.
    #TODO: Change project name and add README.md and add author / date / description
