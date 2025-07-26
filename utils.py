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

def find_mock_job(skills, title, city, country):
    return f"""
    Job Title: {title}
    Location: {city}, {country}
    Description: We're hiring a {title} with experience in {skills}.
    """
