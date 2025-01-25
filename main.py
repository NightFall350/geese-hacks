import streamlit as st

# Title and description
st.title("Job Skills Gap Analyzer")
st.write("Identify the gaps between your skills and job posting requirements with this simple app.")

# Step 1: Input Section
st.header("Step 1: Upload Inputs")

# Upload Resume
uploaded_file = st.file_uploader(
    "Upload your resume (PDF or DOCX format only):",
    type=["pdf", "docx"]
)

# Job Posting Input
job_posting_input = st.text_area(
    "Paste the job posting description or provide a URL (LinkedIn, Indeed, etc.):"
)

# Display feedback after user uploads files or inputs text
if uploaded_file:
    st.success(f"Resume uploaded: {uploaded_file.name}")
else:
    st.info("Please upload your resume.")

if job_posting_input:
    st.success("Job posting input received.")
else:
    st.info("Please enter a job posting description or URL.")

# Step 2: Basic Input Fields for Name and Age
st.header("Step 2: Provide Basic Details")

# Input fields for name and age
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=1, max_value=120, step=1)

# Analyze Button
if st.button("Analyze"):
    if uploaded_file and job_posting_input:
        st.success("Inputs received! Proceeding to analyze...")
        st.write(f"Hello, {name}! You are {age} years old.")
        # Add further logic for analysis in subsequent steps
    else:
        st.warning("Please ensure both the resume and job posting are provided.")