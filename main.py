import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Backend Functions
def extract_resume_text(file):
    """
    Extract text from an uploaded PDF file.
    """
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def extract_keywords_with_ner(text):
    """
    Extract relevant keywords from the text using spaCy's Named Entity Recognition (NER).
    """
    doc = nlp(text)
    keywords = set()
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "SKILL", "WORK_OF_ART", "FACILITY", "PERSON", "GPE"]:
            keywords.add(ent.text)
    return keywords

def extract_keywords_with_tfidf(text, top_n=10):
    """
    Extract top N keywords using TF-IDF from the given text.
    """
    vectorizer = TfidfVectorizer(stop_words="english", max_features=top_n)
    tfidf_matrix = vectorizer.fit_transform([text])
    keywords = vectorizer.get_feature_names_out()
    return set(keywords)

def extract_relevant_keywords(text):
    """
    Combine NER and TF-IDF to extract the most relevant keywords.
    """
    ner_keywords = extract_keywords_with_ner(text)
    tfidf_keywords = extract_keywords_with_tfidf(text)
    combined_keywords = ner_keywords.union(tfidf_keywords)
    return combined_keywords

# Streamlit Frontend
st.title("Job Skills Gap Analyzer")
st.write("Identify the gaps between your skills and job posting requirements with this simple app.")

# Step 1: Input Section
st.header("Step 1: Upload Inputs")

# Upload Resume
uploaded_file = st.file_uploader("Upload your resume (PDF format only):", type=["pdf"])

# Job Posting Input
job_posting_input = st.text_area("Paste the job posting description here:")

# Step 2: Analyze Button
if st.button("Analyze"):
    if uploaded_file and job_posting_input:
        # Extract resume text
        st.info("Extracting text from resume...")
        resume_text = extract_resume_text(uploaded_file)

        # Extract keywords from the job description
        st.info("Analyzing job description...")
        job_keywords = extract_relevant_keywords(job_posting_input)

        # Extract keywords from the resume
        st.info("Analyzing resume...")
        resume_keywords = extract_relevant_keywords(resume_text)

        # Compare keywords
        matched_keywords = resume_keywords & job_keywords
        missing_keywords = job_keywords - resume_keywords

        # Results Page
        st.header("Results: Skill Gap Analysis")

        # 1. Summary Section
        match_percentage = (len(matched_keywords) / len(job_keywords)) * 100 if job_keywords else 0
        st.subheader("Analysis Summary")
        st.metric("Skill Match Percentage", f"{match_percentage:.2f}%", delta=None)

        # 2. Visualizations
        st.subheader("Visualizations")
        st.write("**Matched vs. Missing Skills**")
        
        skills = ["Matched Skills", "Missing Skills"]
        counts = [len(matched_keywords), len(missing_keywords)]
        
        fig, ax = plt.subplots()
        ax.bar(skills, counts, color=["green", "red"])
        ax.set_ylabel("Count")
        ax.set_title("Skill Comparison")
        st.pyplot(fig)

        # 3. Skill Details
        st.subheader("Detailed Skill Analysis")

        st.write("**Matched Skills**")
        st.write(", ".join(matched_keywords) if matched_keywords else "No matched skills found.")

        st.write("**Missing Skills**")
        st.write(", ".join(missing_keywords) if missing_keywords else "No missing skills found.")

    else:
        st.warning("Please upload a resume and enter a job description.")