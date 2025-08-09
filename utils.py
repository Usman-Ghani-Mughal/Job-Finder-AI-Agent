

# utils.py
def read_cv_file(uploaded_file):
    content = uploaded_file.read()
    return content.decode("utf-8", errors="ignore")

def extract_cv_text_from_pdf(file):
    import fitz  # PyMuPDF
    
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_cv_text_from_docx(file):
    pass

def is_requirements_met(cv_text: str, city: str, country: str) -> bool:
    return all([
        isinstance(cv_text, str) and cv_text.strip(),
        isinstance(city, str) and city.strip(),
        isinstance(country, str) and country.strip(),
    ])

def get_jobs_adzuna(skills, city, country):
    import os
    import requests
    import urllib.parse
    
    ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"
    RESULT_PER_PAGE = 100
    
    if not skills or not city or not country:
        raise ValueError("Skills, city, and country are required.")
    
    print('\033[36m' + "skills " + skills)
    encoded_query = urllib.parse.quote(skills)
    
    #encoded_city = urllib.parse.quote(city)
    encoded_country = urllib.parse.quote(country)


    # Final API URL
    url = (
        f"{ADZUNA_BASE_URL}/gb/search/1"
        f"?app_id={os.getenv('ADZUNA_APP_ID')}"
        f"&app_key={os.getenv('ADZUNA_API_KEY')}" 
        f"&results_per_page={RESULT_PER_PAGE}"
        f"&what_or={encoded_query}"
        f"&location0={encoded_country}")
    
    
    print('\033[36m' + "url " + url)
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise RuntimeError(f"Adzuna API failed: {response.status_code} - {response.text}")
    

def find_mock_job(skills, title, city, country):
    return f"""
    Job Title: {title}
    Location: {city}, {country}
    Description: We're hiring a {title} with experience in {skills}.
    """
