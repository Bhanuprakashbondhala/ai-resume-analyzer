import streamlit as st
import PyPDF2
import re

st.write("FINAL VERSION RUNNING")

# ================= SKILL MAP =================
skill_map = {
    "python": ["python", "pandas", "numpy", "scikit", "sklearn"],
    "sql": ["sql", "mysql", "postgresql", "database"],
    "machine learning": ["machine learning", "regression model", "classification model", "clustering algorithm"],
    "web development": ["django", "flask", "api", "backend"],
    "data analysis": ["data analysis", "visualization", "matplotlib", "seaborn"],
    "frontend": ["react", "javascript", "html", "css", "ui", "frontend"],
    "cloud": ["aws", "amazon web services", "ec2", "s3", "lambda", "azure", "gcp"],
    "devops": ["docker", "kubernetes", "jenkins", "terraform", "deployment", "pipeline"],
    "linux": ["linux", "bash", "shell", "unix"]
}

# ================= UI =================
st.title("🚀 AI Job Fit Analyzer")

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")
resume = st.text_area("📄 Paste your Resume")
job = st.text_area("💼 Paste Job Description")

# ================= BUTTON =================
if st.button("Analyze"):

    with st.spinner("Analyzing..."):

        # -------- CLEAN TEXT --------
        if uploaded_file:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text() or ""
            resume_clean = resume_text.lower()
        else:
            resume_clean = resume.lower()

        job_clean = job.lower()

        # -------- REMOVE SPECIAL CHARS --------
        resume_clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', resume_clean)
        job_clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', job_clean)

        # -------- WORD SPLIT --------
        resume_words = resume_clean.split()
        job_words = job_clean.split()

        # -------- SIMILARITY --------
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        tfidf = TfidfVectorizer().fit_transform([resume_clean, job_clean])
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

         # -------- SKILL DETECTION (IMPROVED LOGIC) --------
        def detect_skills(text, skill_map):
            detected = []

            for skill, keywords in skill_map.items():
                match_count = 0

                for keyword in keywords:
                    if keyword in text:
                        match_count += 1

                if match_count >= 1:
                    detected.append(skill)

            return detected


        resume_skills = detect_skills(resume_clean, skill_map)
        job_skills = detect_skills(job_clean, skill_map)
    resume_matches = [w for w in keywords if w in resume_words]
    job_matches = [w for w in keywords if w in job_words]

    # Resume: at least 1 match
    if len(resume_matches) >= 1:
        resume_skills.append(skill)

    if len(job_matches) == len(keywords):
        job_skills.append(skill)

        # -------- MATCHING --------
        matched_skills = list(set(resume_skills) & set(job_skills))
        missing_skills = list(set(job_skills) - set(resume_skills))

        # -------- SAFETY --------
        if not job_skills:
            missing_skills = ["No recognizable skills in job"]

        elif score < 0.4 and not missing_skills:
            missing_skills.append("Skill mismatch detected")

        # -------- FEEDBACK --------
        def generate_feedback(missing_skills, score):
            if score > 0.7:
                level = "Strong Match ✅"
            elif score > 0.4:
                level = "Moderate Match ⚠️"
            else:
                level = "Low Match ❌"

            feedback = level + "\n\n"

            if missing_skills:
                feedback += "Focus on improving:\n"
                for skill in missing_skills:
                    feedback += f"- {skill}\n"
            else:
                feedback += "No missing skills. Improve project depth."

            return feedback

        feedback = generate_feedback(missing_skills, score)

    # -------- OUTPUT --------
    st.metric("Match Score", f"{round(score * 100, 2)}%")

    st.write("### ✅ Matched Skills")
    st.write(matched_skills)

    st.write("### ❌ Missing Skills")
    st.write(missing_skills)

    st.write("### 💡 Suggestions")
    st.write(feedback)