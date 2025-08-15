# IMPORTS
import utils as ut


def load_prompt(filename):
    with open(f"prompts/{filename}", "r", encoding="utf-8") as f:
        return f.read()

def run_agents(**kwargs):
    # check if function is call for extract text from pdf?
    if "extract_cv_text" in kwargs and kwargs["cv_extension"] == "pdf":
        cv_text = ut.extract_cv_text_from_pdf(kwargs['extract_cv_text'])
        return cv_text
    # check if function is call for extract text from docs?
    elif "extract_cv_text" in kwargs and kwargs["cv_extension"] == "docx":
        cv_text = ut.extract_cv_text_from_docx(kwargs['extract_cv_text'])
    # check if function is call for requirment check
    
    elif "is_requirements_meet" in kwargs:
        return ut.is_requirements_met(kwargs['cv_text'], kwargs['city'], kwargs['country'])
    # check if function is call for extract skills from csv
    
    elif "extract_skills_from_csv_text" in kwargs:
        # TODO: Need to find way to shorten the text of CV so less number of token will use
        cv_text = kwargs['cv_text']
        # 1. Extract Skills
        # TODO: **
        skills = ut.extract_skills_from_csv_text(cv_text)
        #skills = "Python Sql Data Enginering Airflow Pyspark Databricks ADF"
        return skills
    elif "search_jobs" in kwargs:
        # Find Jobs first
        jobs = ut.get_jobs_adzuna(skills=kwargs['skills'], city=kwargs['city'], country=kwargs['country'])
        # Now extract most relevant jobs
        
        # TODO: **
        most_relevant_jobs = ut.extract_most_relevant_jobs(skills=kwargs['skills'],
                                                           city=kwargs['city'],
                                                           country=kwargs['country'],
                                                           jobs=jobs,
                                                           n_relevant_jobs=5
                                                           )
        return most_relevant_jobs
    elif "tailor_cv_cover_letter" in kwargs:
        # tailor_cv_cover_letter, current_cv_text, selected_job
        
        tailored_cv = ut.tailor_current_cv(
            cv_text=kwargs['current_cv_text'],
            job_description=kwargs['selected_job'] 
        )
        cover_letter = ut.generate_cover_letter(
            cv_text=kwargs['current_cv_text'],
            job_description=kwargs['selected_job']
        )
        
        cv_and_cover = {
            "tailored_cv": tailored_cv,
            "cover_letter": cover_letter
        }
        
        return cv_and_cover
        
        
        # most_relevant_jobs = [
        #                         {
        #                             "job_id": 3,
        #                             "title": "Python Data Engineer",
        #                             "description": "Where purpose meets career: Impact That Matters: At Atos you will have to opportunity to contribute to major Data and AI projects that make a positive impact to society and to Atos's contribution to improving citizens' lives. Atos is committed to reducing its absolute Greenhouse gas emissions and environmental impact. This is a newly formed business line, pulling together our Data and AI practices. You will have a key role in this business. You will work across our business internally but more …",
        #                             "company": "Eviden UK International Ltd",
        #                             "salary_max": 60000,
        #                             "salary_min": 60000,
        #                             "job_created_date": "2025-08-07T17:42:59Z",
        #                             "job_category": "IT Jobs",
        #                             "job_url": "https://www.adzuna.co.uk/jobs/land/ad/5342092714?se=CiqCuZt18BG8c8Syzm9eLA&utm_medium=api&utm_source=c7ab82da&v=E7584BDC4EB6DFC7BE3EFCF66152F39ABB7D65F7",
        #                             "job_location": "UK",
        #                             "location_latitude": None,
        #                             "location_longitude": None,
        #                         },
        #                         {
        #                             "job_id": 5,
        #                             "title": "Data Analyst - ESG, Python",
        #                             "description": "Your new role My client is a global investment bank with offices based in central london, and they are looking for a Data Analyst with a background in ESG (Environmental, social, and governance) and Python. What you'll need to succeed Proven experience working as a Data Analyst, ideally with a few years in a professional setting. Hands-on experience in an ESG-focused environment, with a strong understanding of sustainability data. Programming skills in Python and/or R, with working knowledge of…",
        #                             "company": "HAYS",
        #                             "salary_max": 46259.56,
        #                             "salary_min": 46259.56,
        #                             "job_created_date": "2025-08-07T17:43:23Z",
        #                             "job_category": "IT Jobs",
        #                             "job_url": "https://www.adzuna.co.uk/jobs/land/ad/5342092782?se=CiqCuZt18BG8c8Syzm9eLA&utm_medium=api&utm_source=c7ab82da&v=D047D8940DD9FA1418CBE5F0D65AC54A4D97482E",
        #                             "job_location": "South East London, London",
        #                             "location_latitude": 51.451818,
        #                             "location_longitude": -0.02806,
        #                         },
        #                         {
        #                             "job_id": 11,
        #                             "title": "SQL Developer",
        #                             "description": "Do you have experience as an SQL Developer and want to take your career further in a thriving office environment? Are you a strong communicator who works well within a team? Do you understand data pipeline tools and data modelling? Were seeking an SQL Developer to join our expanding Database team in Leeds! In the role, you will: Analyse business requirements through collaboration with stakeholders, IT Management, and the user community Develop new systems, integrate third-party platforms, and m…",
        #                             "company": "JNBentley",
        #                             "salary_max": 41675.66,
        #                             "salary_min": 41675.66,
        #                             "job_created_date": "2025-07-24T19:09:17Z",
        #                             "job_category": "IT Jobs",
        #                             "job_url": "https://www.adzuna.co.uk/jobs/land/ad/5320119079?se=CiqCuZt18BG8c8Syzm9eLA&utm_medium=api&utm_source=c7ab82da&v=3A3B214DB1C50AAD09542A008D1F7794792335CC",
        #                             "job_location": "Yorkshire And The Humber, UK",
        #                             "location_latitude": None,
        #                             "location_longitude": None,
        #                         },
        #                         {
        #                             "job_id": 38,
        #                             "title": "Software Engineer III - Data Engineer - Python, SQL - Senior Associate",
        #                             "description": "Job Description We have an exciting and rewarding opportunity for you to take your software engineering career to the next level. As a Software Engineer III at JPMorgan Chase within Investment Banking, you serve as a seasoned member of an agile team to design and deliver trusted market-leading technology products in a secure, stable, and scalable way. You are responsible for carrying out critical technology solutions across multiple technical areas within various business functions in support o…",
        #                             "company": "J.P. MORGAN-1",
        #                             "salary_max": 71791.3,
        #                             "salary_min": 71791.3,
        #                             "job_created_date": "2025-08-09T08:00:26Z",
        #                             "job_category": "IT Jobs",
        #                             "job_url": "https://www.adzuna.co.uk/jobs/land/ad/5345144261?se=CiqCuZt18BG8c8Syzm9eLA&utm_medium=api&utm_source=c7ab82da&v=FAA13ACABD1F620D9FF8623B1E2BCF938C2CA61F",
        #                             "job_location": "London, UK",
        #                             "location_latitude": None,
        #                             "location_longitude": None,
        #                         },
        #                         {
        #                             "job_id": 42,
        #                             "title": "Data Engineer - SQL and Python",
        #                             "description": "Data Engineer - SQL and Python Location: Remote Pay: market rate Duration: 5 months initially Job Description: The main function of the Data Engineer is to develop, evaluate, test and maintain architectures and data solutions within our organization. The typical Data Engineer executes plans, policies, and practices that control, protect, deliver, and enhance the value of the organization’s data assets. Job Responsibilities: Design, construct, install, test and maintain highly scalable data mana…",
        #                             "company": "Atrium Workforce Solutions Ltd",
        #                             "salary_max": 104000,
        #                             "salary_min": 83200,
        #                             "job_created_date": "2025-07-30T17:47:05Z",
        #                             "job_category": "IT Jobs",
        #                             "job_url": "https://www.adzuna.co.uk/jobs/land/ad/5328436694?se=CiqCuZt18BG8c8Syzm9eLA&utm_medium=api&utm_source=c7ab82da&v=949B6FA2D9EF4475886D868074059890049073F8",
        #                             "job_location": "UK",
        #                             "location_latitude": None,
        #                             "location_longitude": None,
        #                         },
        #                     ]
        return most_relevant_jobs

    # # 2. Find Job (Mock)
    # job_description = find_mock_job(skills, job_title, city, country)

    # # 3. Tailor Resume
    # # tailor_prompt = PromptTemplate.from_template(load_prompt("tailor_resume.txt"))
    
    # tailor_prompt = ChatPromptTemplate.from_messages([
    # ("system", "You are a helpful assistant for resume optimization."),
    # ("human", "Tailor the following CV to better fit this job description:\nCV:\n{cv_text}\nJob Description:\n{job_description}")
    # ])
    
    # tailor_chain = LLMChain(llm=llm, prompt=tailor_prompt)
    # tailored_resume = tailor_chain.run({"cv_text": cv_text, "job_description": job_description})

    # # 4. Cover Letter
    # # cover_prompt = PromptTemplate.from_template(load_prompt("cover_letter.txt")) 
    # cover_prompt = ChatPromptTemplate.from_messages([
    # ("system", "You are a professional career assistant."),
    # ("human", "Generate a personalized cover letter for this job:\nJob:\n{job_description}\nResume:\n{cv_text}")
    # ])
    # cover_chain = LLMChain(llm=llm, prompt=cover_prompt)
    # cover_letter = cover_chain.run({"cv_text": tailored_resume, "job_description": job_description})

    # return {
    #     "skills": skills,
    #     "job_description": job_description,
    #     "tailored_resume": tailored_resume,
    #     "cover_letter": cover_letter
    # }
