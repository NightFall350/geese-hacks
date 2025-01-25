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

        # Results Section
        st.header("Results Page: Skill Gap Analysis")

        # 1. Summary Section
        st.subheader("Analysis Summary")
        st.write("Here's a quick summary of your skills compared to the job posting:")
        st.metric("Skill Match Percentage", "70%", delta="15% Improvement")

        # 2. Visualizations
        st.subheader("Visualizations")
        st.write("**Matched vs. Missing Skills**")

        # Example Bar Chart: Matched vs. Missing Skills
        skills = ["Python", "SQL", "Machine Learning", "Cloud Computing", "Leadership"]
        matched = [1, 1, 0, 0, 1]  # 1 for matched, 0 for missing
        df = pd.DataFrame({"Skills": skills, "Matched": matched})

        # Bar chart
        fig, ax = plt.subplots()
        df.groupby("Matched").size().plot(kind="bar", color=["red", "green"], ax=ax)
        ax.set_xticklabels(["Missing Skills", "Matched Skills"], rotation=0)
        ax.set_ylabel("Count")
        ax.set_title("Matched vs. Missing Skills")
        st.pyplot(fig)

        # 3. Skill Details Section
        st.subheader("Detailed Skill Analysis")

        # Example Data for Matched and Missing Skills
        matched_skills = {"Python": "Expert", "SQL": "Intermediate", "Leadership": "Beginner"}
        missing_skills = {"Machine Learning": "N/A", "Cloud Computing": "N/A"}

        # Matched Skills Table
        st.write("**Matched Skills**")
        st.table(pd.DataFrame.from_dict(matched_skills, orient="index", columns=["Proficiency"]))

        # Missing Skills Table
        st.write("**Missing Skills**")
        st.table(pd.DataFrame.from_dict(missing_skills, orient="index", columns=["Proficiency"]))

        # 4. Recommendations Section
        st.subheader("Recommendations for Upskilling")

        # Example Recommendation List
        recommendations = {
            "Machine Learning": "Take the 'Machine Learning' course on Coursera",
            "Cloud Computing": "Learn AWS or Azure through LinkedIn Learning",
        }

        for skill, suggestion in recommendations.items():
            st.write(f"- **{skill}**: {suggestion}")

        # 5. Download Option
        st.subheader("Download Your Results")
        if st.button("Download Report"):
            # Placeholder for file generation logic
            st.success("Report downloaded successfully!")
    else:
        st.warning("Please ensure both the resume and job posting are provided.")