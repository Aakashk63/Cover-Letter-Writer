import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import pdfplumber
from docx import Document

# --- Load Environment Variables ---
load_dotenv()
API_KEY = os.getenv("AIzaSyBSd16aZEhQZzTprZj7OpK6zy2dsYY6lI4")  
genai.configure(api_key="AIzaSyBSd16aZEhQZzTprZj7OpK6zy2dsYY6lI4")
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Helper Functions ---

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text(file):
    file_type = file.name.split('.')[-1].lower()
    if file_type == "pdf":
        return extract_text_from_pdf(file)
    elif file_type == "docx":
        return extract_text_from_docx(file)
    elif file_type == "txt":
        return file.read().decode("utf-8")
    else:
        st.error("Unsupported file type. Please upload PDF, DOCX, or TXT.")
        return ""

# --- Streamlit App ---

st.title("📄 AI-Powered Cover Letter Writer")
st.write("Upload your resume and enter the job role. The AI will generate a tailored cover letter for you!")

# User Inputs
job_role = st.text_input("Job Role", placeholder="e.g. Data Scientist, Software Engineer")
uploaded_file = st.file_uploader("Upload your Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if st.button("Generate Cover Letter"):
    if not job_role:
        st.warning("Please enter the job role.")
    elif not uploaded_file:
        st.warning("Please upload your resume.")
    else:
        with st.spinner("Extracting resume content..."):
            resume_text = extract_text(uploaded_file)

        prompt_template = f"""
You are an expert HR professional and copywriter. Write a professional, engaging, and personalized cover letter for the following job role: **{job_role}**.

Here is the applicant's resume content for reference:

{resume_text}

Guidelines:
- Use a warm and confident tone.
- Highlight relevant skills and experience.
- Address the cover letter to 'Hiring Manager'.
- Keep it under 350 words.
- Include a strong closing paragraph.
- Do NOT repeat the resume verbatim.

Generate the cover letter below:
"""

        with st.spinner("Generating cover letter..."):
            response = model.generate_content(prompt_template)
            cover_letter = response.text

        st.success("Cover letter generated!")
        edited_cover_letter = st.text_area("✏️ Edit your Cover Letter:", cover_letter, height=400)

        st.download_button(
            label="📥 Download Cover Letter",
            data=edited_cover_letter.encode('utf-8'),
            file_name=f"Cover_Letter_{job_role.replace(' ', '_')}.txt",
            mime="text/plain"
        )
