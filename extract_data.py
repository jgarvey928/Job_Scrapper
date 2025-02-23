import csv
import re
from bs4 import BeautifulSoup

# List of keywords to identify the requirements section
keywords = [
    "requirements", "requirement", "qualifications", "qualification", "required education and experience", 
    "skills/qualifications", "skills/qualification", "must have", "required skills", "desired skills",
    "preferred qualifications", "preferred qualification", "basic qualifications", "basic qualification",
    "essential skills", "essential skill", "job requirements", "job requirement", "job qualifications",
    "job qualification", "required experience", "preferred experience", "required education", "desired qualifications",
    "desired qualification", "experience", "education", "skills", "skill", "must-have", "must haves", "must-have skills",
    "must-have skill", "required", "preferred", "essential", "basic", "necessary", "mandatory", "needed", "desired"
]

# Compile a regular expression pattern to match any of the keywords
keywords_pattern = re.compile('|'.join([re.escape(keyword) for keyword in keywords]), re.IGNORECASE)

all_requirements = []

# Function to check if a string contains any of the keywords
def contains_keywords(text):
    return bool(keywords_pattern.search(text))

def not_single_word(text):
    return ' ' in text

def extract_csv(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        for row in reader:
            collected_text = []

            print(row['Job Title'])
            print(row['Company'])
            # print(row['Date'])
            # print(row['Address'])
            # print(row['Link'])

            # Collect all below here
            
            description = row['Description']
            soup = BeautifulSoup(description, 'html.parser')

            # Find all <strong> elements
            strong_elements = soup.find_all('strong')
            i = 0 
            # Iterate through each <strong> element to find the specific combination
            for strong in strong_elements:
                # Check if the <strong> element contains any of the keywords
                if contains_keywords(strong.get_text(strip=True)):
                    i += 1
                    # collected_text.append("\n" + str(i) + ("*" * 50) + "\n")
                    # collected_text.append(strong.get_text(strip=True))
                    
                    # Collect all sibling elements and text nodes until the next <strong> or end of parent container
                    # for sibling in strong.next_siblings:
                    #     if sibling.name == 'strong':
                    #         break
                    #     if sibling.name in ['p', 'ul', 'li', 'br', 'span']: 
                    #         text1 = sibling.get_text(strip=True)
                    #         if text1:
                    #             collected_text.append(text1)
                    #     elif isinstance(sibling, str):  # Handle text nodes
                    #         text2 = sibling.strip()
                    #         if text2:
                    #             collected_text.append(text2)
                    #     elif sibling.name is None:  # Handle text nodes directly after <strong>
                    #         text3 = sibling.strip()
                    #         if text3:
                    #             collected_text.append(text3)

                    # Collect all sibling elements until the next <strong> or end of parent container
                    for sibling in strong.find_all_next():
                        if sibling.name == 'strong':
                            break
                        if sibling.name in ['p', 'ul', 'li', 'br', 'span']:
                            text1 = sibling.get_text(strip=True)
                            if text1:
                                collected_text.append(text1)
                        # elif isinstance(sibling, str):  # Handle text nodes
                        #     text2 = sibling.strip()
                        #     if text2:
                        #         collected_text.append(text2)
                    
            # # After processing all <strong> elements, collect and print all <li> elements
            # # collected_text.append("\nList Items:")
            # li_elements = soup.find_all('li')
            # for li in li_elements:
            #     collected_text.append(li.get_text(strip=True))

            # # After processing all <strong> elements, collect and print all <span> elements
            # # collected_text.append("\nSpan Items:")
            # span_elements = soup.find_all('span')
            # for span in span_elements:
            #     collected_text.append(span.get_text(strip=True))
                
            collected_text.append("\n__________________________________________________\n")

            
            # Collect above here

            # Remove duplicates from the collected text list
            seen = set()
            unique_collected_text = []
            for section in collected_text:
                if section not in seen:
                    unique_collected_text.append(section)
                    seen.add(section)
                    
            # # Print the unique collected text list using an index-based iteration
            # index = 0
            # while index < len(unique_collected_text):
            #     print(str(index) + " - "+ unique_collected_text[index])
            #     index += 1
            
            # Print the unique collected text list using an index-based iteration
            index = 0
            while index < len(unique_collected_text):
                if (index+2) < len(unique_collected_text):
                    if unique_collected_text[index+1] in unique_collected_text[index] and not_single_word(unique_collected_text[index+1]) :
                        pass
                    elif unique_collected_text[index+2] in unique_collected_text[index] and not_single_word(unique_collected_text[index+2]) :
                        pass
                    else :
                        all_requirements.append(unique_collected_text[index])
                        # print(str(index) + " - "+ unique_collected_text[index])
                else :
                    all_requirements.append(unique_collected_text[index])
                    # print(str(index) + " - "+ unique_collected_text[index])
                index += 1

# Define input and output file names
input_csv = 'job_us_listings1.csv'
output_csv = 'extracted_job_listings.csv'

extract_csv(input_csv, output_csv)

# Remove empty or whitespace-only items from all_requirements
all_requirements = [req for req in all_requirements if req.strip()]

# Open the text file for writing
with open('job_us_requirements2.txt', mode='w', encoding='utf-8') as file:
    for req in all_requirements:
        print("+ "+req)  # Print to console
        file.write(req + "\n")  # Write to text file