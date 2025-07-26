# app.py
import streamlit as st
from utils import read_cv_file
from agents import run_agents

st.title("🤖 Multi-Agent Job Application Assistant")

uploaded_file = st.file_uploader("Upload your CV (PDF or TXT)", type=["pdf", "txt"])
job_title = st.text_input("Target Job Title")
country = st.text_input("Country")
city = st.text_input("City")

if st.button("Run AI Agents"):
    if uploaded_file and job_title:
        cv_text = read_cv_file(uploaded_file)
        with st.spinner("Running agents..."):
            output = run_agents(cv_text, job_title, country, city)

            st.subheader("✅ Extracted Skills")
            st.write(output['skills'])

            st.subheader("✅ Found Job Description")
            st.write(output['job_description'])

            st.subheader("✅ Tailored Resume")
            st.text(output['tailored_resume'])

            st.subheader("✅ Cover Letter")
            st.text(output['cover_letter'])
    else:
        st.warning("Please upload a CV and enter job title.")
