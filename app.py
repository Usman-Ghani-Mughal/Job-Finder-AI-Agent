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
    
    st.subheader("📄 Extracted jobs")
    st.text_area("jobs", st.session_state.jobs, height=300)
    
    # with st.chat_message("assistant"):
    #     st.write("🔎 Finding top matching jobs for you...")
    # api_response = call_adzuna_api(st.session_state.city, st.session_state.country)
    # st.session_state.jobs = find_matching_jobs_agent(llm, st.session_state.skills, api_response)

    # st.session_state.stage = "show_jobs"

# # === Stage 4: Show Top Jobs ===
# if st.session_state.stage == "show_jobs":
#     st.chat_message("assistant").markdown("Here are the **top 5 job matches** for your profile:")
#     for idx, job in enumerate(st.session_state.jobs):
#         with st.chat_message("assistant"):
#             st.markdown(f"**{idx+1}. {job['title']} at {job['company']}**")
#             st.markdown(f"📍 {job['location']}")
#             st.markdown(f"📝 {job['description'][:250]}...")
#             st.markdown(f"[🔗 Job Link]({job['url']})")

#     st.session_state.stage = "select_job"

# # === Stage 5: Ask to Pick a Job ===
# if st.session_state.stage == "select_job":
#     selected_index = st.chat_input("Type the number (1-5) of the job you want to tailor your CV for:")
#     if selected_index and selected_index.strip().isdigit():
#         selected_index = int(selected_index.strip()) - 1
#         if 0 <= selected_index < len(st.session_state.jobs):
#             st.session_state.selected_job = st.session_state.jobs[selected_index]
#             st.session_state.stage = "tailor_cv"

# # === Stage 6: Tailor CV and Cover Letter ===
# if st.session_state.stage == "tailor_cv":
#     st.chat_message("assistant").write("🛠️ Tailoring your CV and creating a cover letter...")
#     st.session_state.tailored_cv = tailor_cv_agent(llm, st.session_state.cv_text, st.session_state.selected_job)
#     st.session_state.cover_letter = cover_letter_agent(llm, st.session_state.tailored_cv, st.session_state.selected_job)

#     st.chat_message("assistant").markdown("✅ Here’s your **Tailored CV**:")
#     st.chat_message("assistant").code(st.session_state.tailored_cv)

#     st.chat_message("assistant").markdown("✉️ And your **Cover Letter**:")
#     st.chat_message("assistant").code(st.session_state.cover_letter)

#     st.session_state.stage = "final_confirm"

# # === Stage 7: Final Confirmation ===
# if st.session_state.stage == "final_confirm":
#     user_reply = st.chat_input("Are you happy with the tailored CV and cover letter? (yes/no)")
#     if user_reply:
#         user_reply = user_reply.strip().lower()
#         if "yes" in user_reply:
#             st.chat_message("assistant").success("🚀 Awesome! Best of luck with your job application!")
#             st.session_state.stage = "done"
#         elif "no" in user_reply:
#             st.chat_message("assistant").warning("Tell me what needs changing. I'll help fix it.")
