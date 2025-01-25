from PyPDF2 import PdfReader

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

# Function to extract skills from text
def extract_skills(text, skills_list):
    """
    Matches skills from the skills list against the input text.
    """
    text = text.lower()
    found_skills = [skill for skill in skills_list if skill.lower() in text]
    return found_skills

# Function to compare resume skills with job skills
def compare_skills(resume_skills, job_skills):
    """
    Compares skills from resume and job description.
    Returns matched and missing skills.
    """
    matched = set(resume_skills) & set(job_skills)
    missing = set(job_skills) - set(resume_skills)
    return matched, missing

if __name__ == "__main__":
    # Path to the resume file
    pdf_path = "Jeremy_AE_Resume.pdf"  # Replace with your resume file path

    # List of skills to match
    skills_list = [
        "Python", "SQL", "Tableau", "Power BI", "Excel", "AWS", 
        "Java", "C++", "R", "Machine Learning", "Deep Learning",
        "Data Analysis", "ETL", "BigQuery", "Airflow", "Docker"
    ]

    # Sample job description
    job_description = """
    Looking for a Data Analyst with expertise in Python, SQL, Tableau, and BigQuery. 
    Experience with Docker and Airflow is a plus.
    """

    # Step 1: Extract text from the resume
    print("Extracting text from resume...")
    resume_text = extract_resume_text(pdf_path)

    # Step 2: Extract skills from the resume
    print("\nExtracting skills from resume...")
    resume_skills = extract_skills(resume_text, skills_list)
    print("Skills Found in Resume:", resume_skills)

    # Step 3: Extract skills from the job description
    print("\nExtracting skills from job description...")
    job_skills = extract_skills(job_description, skills_list)
    print("Skills Found in Job Description:", job_skills)

    # Step 4: Compare skills
    print("\nComparing skills...")
    matched_skills, missing_skills = compare_skills(resume_skills, job_skills)

    # Step 5: Output results
    print("\nMatched Skills:")
    print(matched_skills)

    print("\nMissing Skills:")
    print(missing_skills)
