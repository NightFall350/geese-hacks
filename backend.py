from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from a PDF
def extract_resume_text(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return ""

# Function to extract keywords using spaCy
def extract_keywords_with_spacy(text):
    """
    Extracts keywords using spaCy.
    Focuses on nouns and proper nouns as key entities.
    """
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return set(keywords)

# Function to extract keywords using TF-IDF
def extract_keywords_with_tfidf(documents, top_n=10):
    """
    Extracts top N keywords from a list of documents using TF-IDF.
    """
    vectorizer = TfidfVectorizer(stop_words="english", max_features=top_n)
    tfidf_matrix = vectorizer.fit_transform(documents)
    keywords = vectorizer.get_feature_names_out()
    return set(keywords)

# Function to scrape jobs from Indeed
def scrape_jobs(role, location=""):
    """
    Scrapes job listings for the given role from Indeed.
    """
    role_query = role.replace(" ", "+")
    url = f"https://www.indeed.com/jobs?q={role_query}&l={location}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    job_descriptions = []
    for job_card in soup.find_all("div", class_="job_seen_beacon"):
        title = job_card.find("h2", class_="jobTitle").text.strip() if job_card.find("h2", class_="jobTitle") else "N/A"
        company = job_card.find("span", class_="companyName").text.strip() if job_card.find("span", class_="companyName") else "N/A"
        description = job_card.find("div", class_="job-snippet").text.strip() if job_card.find("div", class_="job-snippet") else ""
        job_descriptions.append({
            "title": title,
            "company": company,
            "description": description
        })

    return job_descriptions

# Function to extract keywords from job descriptions
def extract_job_keywords(job_descriptions):
    """
    Extracts keywords from job descriptions using spaCy and TF-IDF.
    """
    # Combine all job descriptions into one text
    combined_text = " ".join([job["description"] for job in job_descriptions])
    
    # Extract keywords using spaCy
    spacy_keywords = extract_keywords_with_spacy(combined_text)
    
    # Extract keywords using TF-IDF
    tfidf_keywords = extract_keywords_with_tfidf([job["description"] for job in job_descriptions])

    return spacy_keywords.union(tfidf_keywords)  # Combine both sets of keywords

# Function to compare resume keywords with job keywords
def compare_skills_with_keywords(resume_text, job_keywords):
    """
    Compare keywords extracted from resume and job descriptions.
    """
    # Extract keywords from resume
    resume_keywords = extract_keywords_with_spacy(resume_text)
    
    # Find matched and missing keywords
    matched = resume_keywords & job_keywords
    missing = job_keywords - resume_keywords
    return matched, missing

if __name__ == "__main__":
    # Path to the resume file
    pdf_path = "Jeremy_AE_Resume.pdf"  # Replace with your resume file path

    # User-specified role
    desired_role = input("Enter the role you are looking for (e.g., Data Analyst): ")
    location = input("Enter a location (leave blank for all locations): ")

    # Step 1: Extract text from the resume
    print("\nExtracting text from resume...")
    resume_text = extract_resume_text(pdf_path)

    # Step 2: Scrape job descriptions online
    print(f"\nScraping job descriptions for '{desired_role}'...")
    job_descriptions = scrape_jobs(desired_role, location)
    print(f"Found {len(job_descriptions)} jobs.")

    # Step 3: Extract keywords from job descriptions
    print("\nExtracting keywords from job descriptions...")
    job_keywords = extract_job_keywords(job_descriptions)
    print("Job Keywords:", job_keywords)

    # Step 4: Compare resume with job keywords
    print("\nComparing resume keywords with job requirements...")
    matched_keywords, missing_keywords = compare_skills_with_keywords(resume_text, job_keywords)

    # Step 5: Output results
    print("\nMatched Keywords:")
    print(matched_keywords)

    print("\nMissing Keywords:")
    print(missing_keywords)

    # Step 6: Display relevant jobs
    print("\nRelevant Jobs:")
    for job in job_descriptions[:5]:  # Show top 5 jobs
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Description: {job['description']}\n")
