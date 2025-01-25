from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_resume_text(file_path):
    """
    Extract text from a PDF file.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return ""

def extract_keywords_with_ner(text):
    """
    Extract relevant keywords from the text using spaCy's Named Entity Recognition (NER).
    """
    doc = nlp(text)
    keywords = set()
    for ent in doc.ents:
        # Filter entities based on relevance (e.g., skills, organizations, or specific entities)
        if ent.label_ in ["ORG", "PRODUCT", "SKILL", "WORK_OF_ART", "FACILITY", "PERSON", "GPE"]:
            keywords.add(ent.text)
    return keywords

def extract_keywords_with_tfidf(text, top_n=10):
    """
    Extract top N keywords using TF-IDF from the given text.
    """
    # TF-IDF works on a collection of documents, so wrap the text in a list
    vectorizer = TfidfVectorizer(stop_words="english", max_features=top_n)
    tfidf_matrix = vectorizer.fit_transform([text])
    keywords = vectorizer.get_feature_names_out()
    return set(keywords)

def extract_relevant_keywords(job_description):
    """
    Combine NER and TF-IDF to extract the most relevant keywords from a job description.
    """
    # Extract keywords using NER
    ner_keywords = extract_keywords_with_ner(job_description)
    
    # Extract keywords using TF-IDF
    tfidf_keywords = extract_keywords_with_tfidf(job_description)
    
    # Combine both sets of keywords
    combined_keywords = ner_keywords.union(tfidf_keywords)
    return combined_keywords

if __name__ == "__main__":
    # Path to the resume file
    pdf_path = "Mohit_s_Resume(OLD).pdf"  # Replace with your resume file path

    # Step 1: Extract text from the resume
    print("\nExtracting text from resume...")
    resume_text = extract_resume_text(pdf_path)

    # Step 2: Get the job description from the user
    print("\nEnter the job description (paste it below):")
    job_description = input()

    # Step 3: Extract relevant keywords from the job description
    print("\nExtracting relevant keywords from the job description...")
    job_keywords = extract_relevant_keywords(job_description)
    print("\nJob Keywords:", job_keywords)

    # Step 4: Extract relevant keywords from the resume
    print("\nExtracting relevant keywords from the resume...")
    resume_keywords = extract_relevant_keywords(resume_text)
    print("\nResume Keywords:", resume_keywords)

    # Step 5: Compare resume with job keywords
    matched_keywords = resume_keywords & job_keywords
    missing_keywords = job_keywords - resume_keywords

    print("\nMatched Keywords:")
    print(matched_keywords)

    print("\nMissing Keywords:")
    print(missing_keywords)
