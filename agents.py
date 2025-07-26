# agents.py
import os
# from langchain.llms import LlamaCpp
from langchain.chains import LLMChain
#from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from utils import find_mock_job
from langchain.chat_models import AzureChatOpenAI

from dotenv import load_dotenv
load_dotenv()


llm = AzureChatOpenAI(
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0.5,
    max_tokens=1000,
)


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

def run_agents(cv_text, job_title, country, city):
    cv_text = cv_text[:2000]
    # 1. Extract Skills
    # parse_prompt = PromptTemplate.from_template(load_prompt("parse_skills.txt"))
    
    parse_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert resume parser."),
        ("human", "Extract relevant skills from this CV:\n{cv_text}")
    ])
    
    parse_chain = LLMChain(llm=llm, prompt=parse_prompt)    
    skills = parse_chain.run({"cv_text": cv_text})

    # 2. Find Job (Mock)
    job_description = find_mock_job(skills, job_title, city, country)

    # 3. Tailor Resume
    # tailor_prompt = PromptTemplate.from_template(load_prompt("tailor_resume.txt"))
    
    tailor_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant for resume optimization."),
    ("human", "Tailor the following CV to better fit this job description:\nCV:\n{cv_text}\nJob Description:\n{job_description}")
    ])
    
    tailor_chain = LLMChain(llm=llm, prompt=tailor_prompt)
    tailored_resume = tailor_chain.run({"cv_text": cv_text, "job_description": job_description})

    # 4. Cover Letter
    # cover_prompt = PromptTemplate.from_template(load_prompt("cover_letter.txt")) 
    cover_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional career assistant."),
    ("human", "Generate a personalized cover letter for this job:\nJob:\n{job_description}\nResume:\n{cv_text}")
    ])
    cover_chain = LLMChain(llm=llm, prompt=cover_prompt)
    cover_letter = cover_chain.run({"cv_text": tailored_resume, "job_description": job_description})

    return {
        "skills": skills,
        "job_description": job_description,
        "tailored_resume": tailored_resume,
        "cover_letter": cover_letter
    }
