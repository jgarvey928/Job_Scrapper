import csv
import google.generativeai as genai
import docx
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import re
import time

GOOGLE_API_KEY = "AIzaSyAtLFVTbGsSWx30-BMUhBHP-SesZGMF55c"

def read_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_docx(file_path, content):
    doc = docx.Document()
    paragraph = doc.add_paragraph(content)
    
    # Set font to Arial and size to 12
    run = paragraph.runs[0]
    run.font.name = 'Arial'
    run.font.size = Pt(12)
    
    # Add spacing between paragraphs
    paragraph_format = paragraph.paragraph_format
    paragraph_format.space_after = Pt(6)
    paragraph_format.line_spacing = 1.15
    
    doc.save("letters/"+file_path)

def analyze_text_from_file(system_instructions, job_data, cl_template):

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    try:
        # Combine instructions and content into a single string
        prompt = system_instructions + "\n\n" + job_data + "\n\n" + cl_template  # Add a separator for clarity

        response = model.generate_content(prompt)
        print("\n$$$ Response Complete $$$\n")
        return response.text
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return None

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_letters(file_name, letter_count):
    
    input_file = 'scrapped_data/'+file_name+'.csv'
    job_descriptions = []
     
    # Read the CSV file
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        for row in reader:
            # Extract the required fields
            job_info = {
                "Job Title": row["Job Title"],
                "Company": row["Company"],
                "Cleaned": row["Cleaned"]
            }
            print(str(job_info)+"\n")
            job_descriptions.append(job_info)

    # Example usage:
    cl_file_path = "letters/cover_letter_template.txt"

    system_instructions = """I am a recent software engineering graduate looking for work. You are a career coach 
                            with over 20 years experience whose helping me fill in my cover letter for a job.
                            Theres a section in square brackets [] in the cover letter that I want you to fill in. 
                            Fill in the section as instructed inside the brackets and based on the job description. 
                            Make it sound human but professional and enthusiastic. Only fill in the bracketed sections
                            leave the rest alone. Heres the job description followed by my cover letter I want you to help complete..."""
    
    try:
        cl_text_content = read_text_file(cl_file_path)
    except FileNotFoundError as e:
        print(f"Error: File not found at {e.filename}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    count = 0
    for data in job_descriptions:
        if count > letter_count:
            break
        job_data_content = data["Job Title"] + "\n" + data["Company"] + "\n" + data["Cleaned"]
        response = analyze_text_from_file(system_instructions, job_data_content, cl_text_content)
        time.sleep(2)
        if response:
            # Replace spaces and special characters with no spaces in the file name
            job_title = re.sub(r'\W+', '', data["Job Title"].replace(" ", ""))
            company = re.sub(r'\W+', '', data["Company"].replace(" ", ""))
            file_name = f"{job_title}_{company}_letter.docx"
            write_docx(file_name, response)
        else:
            print("Failed to get a response from Gemini.")
        count += 1


if __name__ == '__main__':
    file = 'se_phx_entry_onsite_month_02_23_25'
    generate_letters(file, 2)