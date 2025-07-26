# utils.py
def read_cv_file(uploaded_file):
    content = uploaded_file.read()
    return content.decode("utf-8", errors="ignore")

def find_mock_job(skills, title, city, country):
    return f"""
    Job Title: {title}
    Location: {city}, {country}
    Description: We're hiring a {title} with experience in {skills}.
    """
