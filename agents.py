

# llm = AzureChatOpenAI(
#     openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#     deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
#     api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
#     temperature=0.5,
#     max_tokens=1000,
# )


# # Load LLaMA model
# llm = LlamaCpp(
#     model_path="./llama-models/llama-2-7b-chat.Q4_K_M.gguf",
#     temperature=0.5,
#     max_tokens=2048,
#     context_size=2048,
#     n_gpu_layers=20,
#     n_batch=512,
#     verbose=True,
# )



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
        parse_prompt = ChatPromptTemplate.from_messages([
            ("system", prom.extract_skills_from_cv_text_prompt_system),
            ("human", prom.extract_skills_from_cv_text_prompt_human)
        ])
        
        gpt_4o_mini = AzureChatOpenAI(
                openai_api_key=os.getenv("AZURE_OPENAI_KEY_GPT_4O_MINI"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT_4O_MINI"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                temperature=0.3) # type: ignore
    
        parse_chain = LLMChain(llm=gpt_4o_mini, prompt=parse_prompt)    
        skills = parse_chain.run({"cv_text": cv_text})
        return skills
    elif "search_jobs" in kwargs:
        """
            1: Send Skills, City, country to API call function this will return jobs
            2: Ask LLM to get top 5 Most relavent jobs
            3: return the jobs to UI
        """
        # Find Jobs first
        jobs = ut.get_jobs_adzuna(skills=kwargs['skills'], city=kwargs['city'], country=kwargs['country'])
        return jobs

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
