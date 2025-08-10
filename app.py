# app.py
import streamlit as st
from agents import run_agents

st.set_page_config(page_title="Job Finder Assistant", page_icon="💼")

# Session State Initialization
if "stage" not in st.session_state:
    st.session_state.stage = "greet"
if "cv_text" not in st.session_state:
    st.session_state.cv_text = None
if "city" not in st.session_state:
    st.session_state.city = ""
if "country" not in st.session_state:
    st.session_state.country = ""
if "skills" not in st.session_state:
    st.session_state.skills = None
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "selected_job" not in st.session_state:
    st.session_state.selected_job = None
if "tailored_cv" not in st.session_state:
    st.session_state.tailored_cv = ""
if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = ""

# === Stage 1: Greet user ===
if st.session_state.stage == "greet":
    st.chat_message("assistant").write("👋 Hi! I'm your Job Finder Assistant.\n\nPlease upload your **CV**, and tell me your preferred **city** and **country** for the job search.")
    st.session_state.stage = "ask_inputs"

# === Stage 2: Ask for inputs ===
if st.session_state.stage == "ask_inputs":
    with st.chat_message("user"):
        uploaded_cv = st.file_uploader("Upload your CV", type=["pdf", "docx"])
        city = st.text_input("Preferred City")
        country = st.text_input("Preferred Country")

    if uploaded_cv and city and country:
        with st.chat_message("assistant"):
            st.write("Processing your inputs...")

        # First we need to extract CV text
        file_name = uploaded_cv.name
        extension = extension = file_name.split(".")[-1].lower()
        cv_text = ""
        if extension == "pdf":
            # Extract text from PDF
            cv_text = run_agents(extract_cv_text = uploaded_cv, cv_extension = "pdf")
        elif extension == "docx":
            # Extract text from DOCX
            cv_text = run_agents(extract_cv_text = uploaded_cv, cv_extension = "docx")
        else:
            st.error("Unsupported file type.")
        
        st.session_state.cv_text = cv_text
        st.session_state.city = city
        st.session_state.country = country

        # check if all requirement is meet or not
        if not run_agents(is_requirements_meet=True, 
                          cv_text=st.session_state.cv_text, 
                          city=st.session_state.city, 
                          country=st.session_state.country):
            st.chat_message("assistant").error("All fields are required.")
        else:
            # TODO: I comment this becuase if i want to check if text from cv is been extracted or not
            # st.subheader("📄 Extracted CV Text")
            # st.text_area("CV Content", st.session_state.cv_text, height=300)
            st.session_state.stage = "extract_skills"

# === Stage 3: Extract Skills ===
if st.session_state.stage == "extract_skills":
    with st.chat_message("assistant"):
        st.write("🔍 Analyzing your CV for skills...")
    st.session_state.skills = run_agents(extract_skills_from_csv_text=True, cv_text = st.session_state.cv_text)
    st.session_state.stage = "search_matching_jobs"
    # TODO: I commented this because if i want to check if skills are extracting correct or not
    st.subheader("📄 Extracted skills")
    st.text_area("skills", st.session_state.skills, height=300)
    
# === Stage 3: Fetch Matching Jobs ===
if st.session_state.stage == "search_matching_jobs":
    with st.chat_message("assistant"):
        st.write("🔎 Finding top matching jobs for you...")
        
    # get matching jobs 
    st.session_state.jobs = run_agents(search_jobs = True, 
                                       skills=st.session_state.skills,
                                       city=st.session_state.city,
                                       country=st.session_state.country)
    
    # st.subheader("📄 Extracted jobs")
    # st.text_area("jobs", st.session_state.jobs, height=300)
    
    st.subheader("💼 Matching Jobs")
    
    selected_job_id = None

    for i, job in enumerate(st.session_state.jobs):
        with st.expander(f"{job['title']} at {job['company']} ({job['job_location']})", expanded=False):
            st.write(f"**Company:** {job['company']}")
            st.write(f"**Location:** {job['job_location']}")
            st.write(f"**Salary:** £{job['salary_min']} - £{job['salary_max']}")
            st.write(f"**Description:**\n{job['description']}")
            st.markdown(f"[View Job Posting]({job['job_url']})")
            
            # Radio button inside expander to select this job
            if st.radio("Select this job?", ("No", "Yes"), key=f"select_job_{i}") == "Yes":
                selected_job_id = job['job_id']

    if selected_job_id is not None:
        selected_job = next(job for job in st.session_state.jobs if job['job_id'] == selected_job_id)
        st.session_state.selected_job = selected_job
        st.session_state.stage = "genrate_cv_and_cover_letter_confirmation"

if st.session_state.stage == "genrate_cv_and_cover_letter_confirmation":
    st.subheader("Thanks for selecting the job now do you want to Generate tailored CV & Cover Letter ")
    if st.button("Generate tailored CV & Cover Letter"):
        st.session_state.stage = "generate_documents"
        # st.experimental_rerun()
    else:
        st.info("Please select one job by choosing 'Yes' under the job you want to apply for.")

if st.session_state.stage == "generate_documents":
    st.subheader("Here is your genrated document")

    # st.subheader("📄 Extracted jobs")
    # st.text_area("jobs", st.session_state.jobs, height=300)