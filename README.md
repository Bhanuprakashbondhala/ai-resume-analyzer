# AI Resume Analyzer

An NLP-based web application that analyzes resumes, extracts key skills, and evaluates candidate relevance based on job requirements.

##  Overview
This project uses Natural Language Processing (NLP) techniques to automate resume screening by identifying skills, keywords, and matching them against job descriptions.

##  Features
- Resume parsing from PDF files
- Skill extraction using spaCy NLP
- Keyword-based matching with job descriptions
- Resume scoring system
- Interactive web interface using Streamlit

##  Tech Stack
- Python
- Streamlit
- spaCy (NLP)
- PyPDF2
- Regular Expressions

##  How It Works
1. Upload your resume (PDF format)
2. System extracts text and processes it
3. Identifies skills and keywords
4. Compares with job description
5. Generates a score and insights

##  Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
