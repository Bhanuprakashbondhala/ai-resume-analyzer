import streamlit as st
import PyPDF2
import re

# ================= EXPANDED SKILL MAP =================
skill_map = {
    # Programming Languages
    "python": ["python", "pandas", "numpy", "scikit", "sklearn", "scipy", "jupyter", "pip", "conda"],
    "java": ["java", "spring", "maven", "gradle", "jvm", "hibernate"],
    "javascript": ["javascript", "js", "nodejs", "node js", "typescript", "ts", "es6"],
    "c++": ["c++", "cpp", "c plus plus"],
    "r language": ["r programming", "ggplot", "dplyr", "tidyverse", "shiny"],
    "go": ["golang", "go language"],
    "ruby": ["ruby", "rails", "ruby on rails"],
    "php": ["php", "laravel", "symfony"],
    "swift": ["swift", "xcode", "ios development"],
    "kotlin": ["kotlin", "android development"],

    # Data Science & AI
    "machine learning": ["machine learning", "ml", "regression", "classification", "clustering", "random forest", "xgboost", "lightgbm", "supervised", "unsupervised"],
    "deep learning": ["deep learning", "neural network", "cnn", "rnn", "lstm", "transformer", "bert", "gpt", "pytorch", "tensorflow", "keras"],
    "nlp": ["nlp", "natural language processing", "text mining", "sentiment analysis", "tokenization", "named entity"],
    "computer vision": ["computer vision", "image recognition", "object detection", "opencv", "yolo"],
    "data science": ["data science", "data scientist", "predictive modeling", "feature engineering", "model deployment"],
    "data analysis": ["data analysis", "data analyst", "matplotlib", "seaborn", "visualization", "tableau", "power bi", "excel", "pivot", "reporting"],
    "statistics": ["statistics", "statistical analysis", "hypothesis testing", "a b testing", "probability", "correlation"],

    # Databases
    "sql": ["sql", "mysql", "postgresql", "sqlite", "oracle", "mssql", "sql server", "stored procedure", "query optimization"],
    "nosql": ["nosql", "mongodb", "cassandra", "redis", "elasticsearch", "dynamodb", "couchdb", "firebase"],
    "data engineering": ["data engineering", "etl", "data pipeline", "airflow", "spark", "hadoop", "kafka", "hive", "databricks", "snowflake", "bigquery"],

    # Web Development
    "frontend": ["frontend", "react", "reactjs", "angular", "vue", "vuejs", "html", "css", "sass", "tailwind", "bootstrap", "next js", "nextjs"],
    "backend": ["backend", "django", "flask", "fastapi", "rest api", "graphql", "express", "spring boot", "node js", "microservices"],
    "web development": ["web development", "web application", "responsive design", "ui ux", "api development"],

    # Cloud & Infrastructure
    "cloud": ["cloud", "aws", "amazon web services", "ec2", "s3", "lambda", "rds", "cloudformation", "azure", "gcp", "google cloud", "cloud computing"],
    "devops": ["devops", "docker", "kubernetes", "k8s", "jenkins", "terraform", "ansible", "ci cd", "gitlab ci", "github actions", "helm"],
    "linux": ["linux", "ubuntu", "centos", "bash", "shell", "shell scripting", "unix", "command line"],

    # Tools & Practices
    "git": ["git", "github", "gitlab", "bitbucket", "version control", "branching"],
    "agile": ["agile", "scrum", "kanban", "sprint", "jira", "confluence", "project management"],
    "testing": ["testing", "unit test", "pytest", "selenium", "test automation", "qa", "quality assurance"],
    "system design": ["system design", "distributed system", "scalability", "load balancing", "caching", "high availability"],

    # Soft Skills / Domain
    "communication": ["communication", "presentation", "stakeholder", "documentation", "technical writing"],
    "leadership": ["leadership", "team lead", "mentoring", "people management", "cross functional"],
    "cybersecurity": ["cybersecurity", "security", "penetration testing", "owasp", "encryption", "authentication", "oauth"],
    "blockchain": ["blockchain", "ethereum", "solidity", "smart contract", "web3"],
    "iot": ["iot", "internet of things", "embedded systems", "arduino", "raspberry pi"],
}

# ================= UI =================
st.set_page_config(page_title="AI Resume Intelligence System", layout="wide")
st.title("AI Resume Intelligence System")
st.markdown("### Analyze Your Resume vs Job Description")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")
    resume = st.text_area("Or paste your Resume here", height=300)

with col2:
    job = st.text_area("💼 Paste Job Description here", height=350)

# ================= ANALYZE BUTTON =================
if st.button("Analyze Now", use_container_width=True):

    with st.spinner("Analyzing your resume against job description..."):

        # -------- HANDLE PDF --------
        if uploaded_file:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text() or ""
            resume_clean = resume_text.lower()
        elif resume.strip():
            resume_clean = resume.lower()
        else:
            st.error("Please upload a PDF resume or paste your resume text.")
            st.stop()

        if not job.strip():
            st.error("Please paste a job description.")
            st.stop()

        job_clean = job.lower()

        # -------- CLEAN TEXT --------
        resume_clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', resume_clean)
        job_clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', job_clean)

        # Normalize
        resume_clean = re.sub(r'\s+', ' ', resume_clean).strip()
        job_clean = re.sub(r'\s+', ' ', job_clean).strip()

        # -------- SKILL DETECTION: RESUME --------
        def detect_skills(text, skill_map):
            detected = []
            text = " " + text + " "
            for skill, keywords in skill_map.items():
                for keyword in keywords:
                    if f" {keyword.lower()} " in text:
                        detected.append(skill)
                        break  # One match is enough per skill
            return list(set(detected))

        # -------- SKILL DETECTION: JOB --------
        def detect_job_skills(text, skill_map):
            detected = []
            text = " " + text + " "
            for skill, keywords in skill_map.items():
                for keyword in keywords:
                    if f" {keyword.lower()} " in text:
                        detected.append(skill)
                        break  # One match is enough per skill
            return list(set(detected))

        resume_skills = detect_skills(resume_clean, skill_map)
        job_skills = detect_job_skills(job_clean, skill_map)

        # -------- MATCHING --------
        matched_skills = sorted(list(set(resume_skills) & set(job_skills)))
        missing_skills = sorted(list(set(job_skills) - set(resume_skills)))
        extra_skills = sorted(list(set(resume_skills) - set(job_skills)))

        # -------- SCORING --------
        if len(job_skills) == 0:
            score = 0.0
        else:
            skill_score = len(matched_skills) / len(job_skills)
            resume_strength = len(matched_skills) / max(len(resume_skills), 1)
            score = (0.7 * skill_score) + (0.3 * resume_strength)
            score = min(score, 1.0)

        # -------- FEEDBACK --------
        def generate_feedback(missing_skills, score, matched_skills, job_skills):
            feedback_lines = []

            if not job_skills:
                return "⚠️ Could not detect recognizable skills in the job description. Try adding more technical keywords."

            if score > 0.75:
                feedback_lines.append("🌟 **Excellent profile match!** You are a strong candidate for this role.")
            elif score > 0.5:
                feedback_lines.append("✅ **Good match!** You meet many of the requirements. A few improvements can strengthen your profile.")
            elif score > 0.3:
                feedback_lines.append("⚠️ **Moderate match.** You meet some requirements but there are significant skill gaps to address.")
            else:
                feedback_lines.append("❌ **Low match.** Your resume needs significant improvement for this role.")

            if missing_skills:
                feedback_lines.append("\n**Skills to learn or add to your resume:**")
                for skill in missing_skills:
                    tips = {
                        "python": "📘 Learn Python — focus on Pandas, NumPy, and Scikit-learn for data roles.",
                        "sql": "🗄️ Practice SQL queries, joins, and stored procedures. Try LeetCode SQL.",
                        "machine learning": "🤖 Study ML fundamentals — regression, classification, model evaluation.",
                        "deep learning": "🧠 Learn PyTorch or TensorFlow. Try fast.ai for practical deep learning.",
                        "data analysis": "📊 Master Excel, Tableau, or Power BI for data analysis and visualization.",
                        "cloud": "☁️ Get certified in AWS, Azure, or GCP. Start with free tier accounts.",
                        "devops": "⚙️ Learn Docker, Kubernetes, and CI/CD pipelines (GitHub Actions or Jenkins).",
                        "linux": "🐧 Practice Linux command line. Try Ubuntu on WSL or a VM.",
                        "git": "🔀 Learn Git branching, pull requests, and version control workflows.",
                        "javascript": "🌐 Learn JavaScript and a modern framework like React or Vue.",
                        "nosql": "📦 Learn MongoDB or Redis. Great for modern backend and cloud roles.",
                        "data engineering": "🔧 Learn Spark, Kafka, and cloud data tools like Snowflake or BigQuery.",
                        "system design": "🏗️ Study distributed systems, caching, and scalability. Read 'Designing Data-Intensive Applications'.",
                        "nlp": "💬 Explore NLP with Hugging Face Transformers or spaCy.",
                        "cybersecurity": "🔐 Learn OWASP top 10, authentication patterns, and ethical hacking basics.",
                        "testing": "✅ Learn pytest, Selenium, and test-driven development (TDD).",
                        "agile": "🏃 Get familiar with Scrum/Kanban. Consider a Scrum Master certification.",
                    }
                    feedback_lines.append(f"- {tips.get(skill, f'📚 Study and build projects in: **{skill}**')}")

            if extra_skills:
                feedback_lines.append(f"\n💡 **You have {len(extra_skills)} extra skill(s)** not required by this job: {', '.join(extra_skills[:5])}{'...' if len(extra_skills) > 5 else ''}")

            return "\n".join(feedback_lines)

        feedback = generate_feedback(missing_skills, score, matched_skills, job_skills)

    # ================= OUTPUT =================
    st.markdown("---")
    st.subheader("📊 Analysis Results")

    # Score Row
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("🎯 Match Score", f"{round(score * 100, 1)}%")
    with col_b:
        st.metric("✅ Matched Skills", len(matched_skills))
    with col_c:
        st.metric("❌ Missing Skills", len(missing_skills))

    st.progress(score)

    # Verdict
    if score > 0.75:
        st.success("🌟 Excellent Match — Highly Recommended for Interview")
    elif score > 0.5:
        st.success("✅ Good Match — Recommended for Interview")
    elif score > 0.3:
        st.warning("⚠️ Moderate Match — Consider with Improvements")
    else:
        st.error("❌ Low Match — Significant Skill Gaps Detected")

    st.markdown("---")

    # Skills Columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ✅ Matched Skills")
        if matched_skills:
            for s in matched_skills:
                st.success(f"✔ {s.title()}")
        else:
            st.write("No matched skills found.")

    with col2:
        st.markdown("### ❌ Missing Skills")
        if missing_skills:
            for s in missing_skills:
                st.error(f"✘ {s.title()}")
        else:
            st.write("No missing skills! Great job.")

    with col3:
        st.markdown("### 🔵 Extra Skills in Resume")
        if extra_skills:
            for s in extra_skills:
                st.info(f"+ {s.title()}")
        else:
            st.write("No extra skills detected.")

    st.markdown("---")

    # Skill Coverage
    if job_skills:
        coverage = (len(matched_skills) / len(job_skills)) * 100
        st.markdown(f"### 📈 Skill Coverage: **{round(coverage, 1)}%** of job requirements matched")
        st.progress(coverage / 100)

    # Feedback
    st.markdown("---")
    st.markdown("### 💡 Personalized Feedback & Recommendations")
    st.markdown(feedback)