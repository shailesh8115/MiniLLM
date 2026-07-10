# import streamlit as st
# import sqlite3
# import smtplib
# from io import BytesIO
# from docx import Document
# from pypdf import PdfReader
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from email.message import EmailMessage

# from rag import (
#     ask_resume,
#     analyze_resume,
#     skill_growth,
#     generate_resume,
#     jd_match,
#     extract_resume_data
# )

# # =========================
# # DB SETUP
# # =========================
# conn = sqlite3.connect("resume.db", check_same_thread=False)
# c = conn.cursor()

# c.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     username TEXT PRIMARY KEY,
#     password TEXT
# )
# """)

# c.execute("""
# CREATE TABLE IF NOT EXISTS resumes (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT,
#     resume TEXT
# )
# """)

# conn.commit()

# # =========================
# # SESSION
# # =========================
# if "user" not in st.session_state:
#     st.session_state.user = None

# # =========================
# # AUTH FUNCTIONS
# # =========================
# def signup(username, password):
#     try:
#         c.execute("INSERT INTO users VALUES (?,?)", (username, password))
#         conn.commit()
#         return True
#     except:
#         return False


# def login(username, password):
#     c.execute(
#         "SELECT * FROM users WHERE username=? AND password=?",
#         (username, password)
#     )
#     return c.fetchone()


# def save_resume(username, resume_text):
#     c.execute(
#         "INSERT INTO resumes (username, resume) VALUES (?,?)",
#         (username, resume_text)
#     )
#     conn.commit()

# # =========================
# # EMAIL FUNCTION
# # =========================
# def send_email(to_email, subject, body, docx_file, pdf_file):

#     EMAIL_ADDRESS = "yourgmail@gmail.com"
#     EMAIL_PASSWORD = "your_app_password"

#     msg = EmailMessage()
#     msg["Subject"] = subject
#     msg["From"] = EMAIL_ADDRESS
#     msg["To"] = to_email

#     msg.set_content(body)

#     msg.add_attachment(
#         docx_file.read(),
#         maintype="application",
#         subtype="vnd.openxmlformats-officedocument.wordprocessingml.document",
#         filename="resume.docx"
#     )

#     msg.add_attachment(
#         pdf_file.read(),
#         maintype="application",
#         subtype="pdf",
#         filename="resume.pdf"
#     )

#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#         smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#         smtp.send_message(msg)

# # =========================
# # FILE HELPERS
# # =========================
# def create_docx(text):
#     doc = Document()
#     doc.add_heading("Resume", 0)
#     doc.add_paragraph(text)

#     buffer = BytesIO()
#     doc.save(buffer)
#     buffer.seek(0)
#     return buffer


# def create_pdf(text):
#     buffer = BytesIO()
#     pdf = SimpleDocTemplate(buffer)
#     styles = getSampleStyleSheet()

#     content = []
#     for line in text.split("\n"):
#         if line.strip():
#             content.append(Paragraph(line, styles["BodyText"]))
#             content.append(Spacer(1, 5))

#     pdf.build(content)
#     buffer.seek(0)
#     return buffer

# # =========================
# # LOGIN PAGE
# # =========================
# if st.session_state.user is None:

#     st.title("🔐 Login / Signup")

#     tabA, tabB = st.tabs(["Login", "Signup"])

#     with tabA:
#         u = st.text_input("Username")
#         p = st.text_input("Password", type="password")

#         if st.button("Login"):
#             user = login(u, p)
#             if user:
#                 st.session_state.user = u
#                 st.success("Login successful")
#                 st.rerun()
#             else:
#                 st.error("Invalid login")

#     with tabB:
#         u2 = st.text_input("New Username")
#         p2 = st.text_input("New Password", type="password")

#         if st.button("Create Account"):
#             if signup(u2, p2):
#                 st.success("Account created")
#             else:
#                 st.error("User already exists")

#     st.stop()

# # =========================
# # MAIN APP
# # =========================
# st.title("🚀 AI Resume Suite")

# tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
#     "💬 Chat",
#     "📊 ATS",
#     "📈 Growth",
#     "📝 Builder",
#     "🎯 JD Match",
#     "📊 Dashboard"
# ])

# # =========================
# # CHAT
# # =========================
# with tab1:
#     q = st.text_input("Ask resume question")

#     if st.button("Ask"):
#         if q:
#             with st.spinner("Thinking..."):
#                 ans = ask_resume(q)
#             st.write(ans)

# # =========================
# # ATS
# # =========================
# with tab2:
#     if st.button("Analyze Resume"):
#         with st.spinner("Analyzing..."):
#             result = analyze_resume()
#         st.markdown(result)

# # =========================
# # GROWTH
# # =========================
# with tab3:
#     if st.button("Generate Plan"):
#         with st.spinner("Working..."):
#             result = skill_growth()
#         st.markdown(result)

# # =========================
# # BUILDER
# # =========================
# with tab4:

#     st.subheader("📝 Resume Builder")

#     # FIXED VARIABLES
#     auto_name = ""
#     auto_email = ""
#     auto_phone = ""

#     uploaded = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

#     if uploaded:
#         text = ""
#         reader = PdfReader(uploaded)

#         for page in reader.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text

#         extracted = extract_resume_data(text)

#         auto_name = extracted.get("name", "")
#         auto_email = extracted.get("email", "")
#         auto_phone = extracted.get("phone", "")

#         st.success("Resume Parsed")

#     template = st.selectbox("Template", ["Modern", "Professional", "Harvard"])

#     name = st.text_input("Name", auto_name)
#     email = st.text_input("Email", auto_email)
#     phone = st.text_input("Phone", auto_phone)
#     role = st.text_input("Role", "Computer Vision Engineer")

#     education = st.text_area("Education")
#     certs = st.text_area("Certifications")
#     skills = st.text_area("Skills")
#     exp = st.text_area("Experience")
#     projects = st.text_area("Projects")

#     send_to_email = st.text_input("Send Resume To Email (optional)")

#     st.subheader("📄 Live Preview")
#     st.info("Preview is simplified (safe mode)")

#     st.text(f"""
# {name}
# {role}
# {email} | {phone}

# Skills:
# {skills}

# Experience:
# {exp}

# Projects:
# {projects}

# Education:
# {education}
# """)

#     if st.button("🚀 Generate Resume"):

#         with st.spinner("Generating..."):
#             resume = generate_resume(
#                 template,
#                 name,
#                 email,
#                 phone,
#                 role,
#                 skills,
#                 exp,
#                 projects,
#                 education,
#                 certs
#             )

#         st.success("Done")
#         st.markdown(resume)

#         save_resume(st.session_state.user, resume)

#         docx = create_docx(resume)
#         pdf = create_pdf(resume)

#         st.download_button("Download DOCX", docx, "resume.docx")
#         st.download_button("Download PDF", pdf, "resume.pdf")

#         if send_to_email:
#             send_email(
#                 send_to_email,
#                 "Your AI Resume",
#                 "Attached resume",
#                 docx,
#                 pdf
#             )
#             st.success("Email sent")

# # =========================
# # JD MATCH
# # =========================
# with tab5:
#     jd = st.text_area("Paste Job Description")

#     if st.button("Match"):
#         if jd:
#             with st.spinner("Matching..."):
#                 result = jd_match(jd)
#             st.markdown(result)

# # =========================
# # DASHBOARD
# # =========================
# with tab6:
#     st.subheader("📊 My Saved Resumes")

#     c.execute(
#         "SELECT resume FROM resumes WHERE username=?",
#         (st.session_state.user,)
#     )

#     data = c.fetchall()

#     if data:
#         for i, r in enumerate(data):
#             st.markdown(f"### Resume {i+1}")
#             st.text(r[0][:500])
#     else:
#         st.info("No resumes saved yet.")
import streamlit as st
import tempfile
from rag import rag
from resume import analyze_resume
# ==========================================
# IMPORT MODULES
# ==========================================

from auth import (
    login_page,
    logout
)

from dashboard import (
    home_page
)

from rag import rag

from memory import memory

from database import (
    create_tables,
    load_chat,
    clear_chat,
    dashboard_stats
)

from resume import (
    analyze_resume,
    skill_growth,
    generate_resume,
    improve_resume,
    jd_match,
    extract_resume_data
)

from utils import (
    create_docx,
    create_pdf
)

from ocr import ocr
from websearch import web


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="MiniLLM AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# LOCAL CSS
# ==========================================

from pathlib import Path

def local_css():

    css_file = Path("assets/style.css")

    if css_file.exists():

        with open(css_file, "r") as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    else:

        st.warning("assets/style.css not found. Running with default theme.")

# ==========================================
# DATABASE
# ==========================================

create_tables()


# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False


# ==========================================
# LOGIN
# ==========================================

if not st.session_state.logged_in:

    login_page()

    st.stop()
    # ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
        width=90
    )

    st.title("🤖 MiniLLM")

    st.caption(
        f"Welcome, **{st.session_state.user}** 👋"
    )

    st.divider()

    # ======================================
    # PDF Upload (RAG)
    # ======================================

    # uploaded_files = st.file_uploader(
    #     "📄 Upload PDF Documents",
    #     type=["pdf"],
    #     accept_multiple_files=True,
    #     key="sidebar_pdf_upload"
    # )

    # if uploaded_files:

    #     with st.spinner("📚 Indexing Documents..."):

    #         for pdf in uploaded_files:

    #             with tempfile.NamedTemporaryFile(
    #                 delete=False,
    #                 suffix=".pdf"
    #             ) as tmp:

    #                 tmp.write(pdf.read())

    #                 rag.add_document(tmp.name)

    #     st.session_state.documents_loaded = True

    #     st.success("✅ Documents Indexed Successfully")

    # st.divider()

    # ======================================
    # NAVIGATION
    # ======================================

    st.subheader("📂 Navigation")

    pages = [
        "Dashboard",
        "AI Chat",
        "Resume Builder",
        "ATS Checker",
        "Skill Growth",
        "JD Match",
        "OCR",
        "Web Search",
        "Settings"
    ]

    icons = {
        "Dashboard": "🏠",
        "AI Chat": "💬",
        "Resume Builder": "📝",
        "ATS Checker": "📊",
        "Skill Growth": "📈",
        "JD Match": "🎯",
        "OCR": "🖼",
        "Web Search": "🌐",
        "Settings": "⚙️"
    }

    current = pages.index(st.session_state.page)

    selected = st.radio(
        "Go To",
        pages,
        index=current,
        format_func=lambda x: f"{icons[x]}  {x}"
    )

    st.session_state.page = selected

    st.divider()

    # ======================================
    # QUICK STATS
    # ======================================

    stats = dashboard_stats(
        st.session_state.user
    )

    st.subheader("📊 Statistics")

    st.metric(
        "💬 Chats",
        stats["chats"]
    )

    st.metric(
        "📄 PDFs",
        rag.count()
    )

    st.metric(
        "📝 Resumes",
        stats["resumes"]
    )

    st.metric(
        "🌐 Searches",
        stats["searches"]
    )

    st.metric(
        "🖼 OCR Files",
        stats["ocr"]
    )

    st.divider()

    # ======================================
    # CHAT ACTIONS
    # ======================================

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):

        clear_chat(
            st.session_state.user
        )

        memory.clear(
            st.session_state.user
        )

        st.session_state.messages = []

        st.success("Chat Cleared")

        st.rerun()

    # ======================================
    # LOGOUT
    # ======================================

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()
        # ==========================================================
# PAGE ROUTING
# ==========================================================

if st.session_state.page == "Dashboard":

    home_page()

# ==========================================================
# AI CHAT
# ==========================================================

elif st.session_state.page == "AI Chat":

    st.title("💬 Resume AI Chat")
    st.caption("Upload your resume and chat with AI.")

    # -----------------------------
    # Upload Resume
    # -----------------------------
    # ==========================================
# Resume Upload
# ==========================================

uploaded_resume = st.file_uploader(
    "📄 Upload Resume (PDF)",
    type=["pdf"],
    key="resume_chat"
)

if uploaded_resume is not None:

    current_file = (
        uploaded_resume.name
        + "_"
        + str(uploaded_resume.size)
    )

    if st.session_state.get("resume_file") != current_file:

        try:

            with st.spinner("📚 Reading Resume..."):

                rag.clear()

                rag.add_document(uploaded_resume)

                st.session_state.resume_loaded = True
                st.session_state.resume_file = current_file

            st.success("✅ Resume uploaded successfully!")

        except Exception as e:

            st.session_state.resume_loaded = False

            st.error(f"❌ Failed to upload resume.\n\n{e}")

st.divider()

# ==========================================
# Load Previous Chat
# ==========================================

if len(st.session_state.messages) == 0:

    history = load_chat(st.session_state.user)

    for q, a in history:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": q
            }
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": a
            }
        )

# ==========================================
# Display Chat
# ==========================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# Chat Input
# ==========================================

prompt = st.chat_input("Ask about your resume...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("🤖 Thinking..."):

            try:

                if st.session_state.get("resume_loaded", False):

                    answer = rag.ask(prompt)

                else:

                    answer = (
                        "⚠️ Please upload your resume first."
                    )

            except Exception as e:

                answer = f"❌ Error: {e}"

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    memory.save(
        st.session_state.user,
        prompt,
        answer
    )

# ==========================================================
# RESUME BUILDER
# ==========================================================

# ==========================================================
# RESUME BUILDER
# ==========================================================

elif st.session_state.page == "Resume Builder":

    st.title("📝 AI Resume Builder")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    location = st.text_input("Location")
    linkedin = st.text_input("LinkedIn")
    github = st.text_input("GitHub")

    education = st.text_area("Education")
    experience = st.text_area("Experience")
    skills = st.text_area("Skills")
    projects = st.text_area("Projects")

    if st.button("🚀 Generate Resume"):

        resume_text = generate_resume({

            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "linkedin": linkedin,
            "github": github,
            "education": education,
            "experience": experience,
            "skills": skills,
            "projects": projects

        })

        st.subheader("Preview")

        st.text_area(
            "Resume",
            resume_text,
            height=450
        )

        docx_data = create_docx(resume_text)

        pdf_data = create_pdf(resume_text)

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                "📄 Download DOCX",
                data=docx_data,
                file_name="resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        with col2:

            st.download_button(
                "📕 Download PDF",
                data=pdf_data,
                file_name="resume.pdf",
                mime="application/pdf"
            )
# ==========================================================
# ATS CHECKER
# ==========================================================

# ==========================================================
# ATS CHECKER
# ==========================================================
elif st.session_state.page == "ATS Checker":

    import re
    import tempfile

    st.title("📊 ATS Resume Checker")

    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

    if resume:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:

            tmp.write(resume.read())
            pdf_path = tmp.name

        with st.spinner("📖 Reading Resume..."):
            resume_text = rag.read_pdf(pdf_path)

        with st.spinner("🤖 Analyzing Resume..."):
            result = analyze_resume(resume_text)

        # -----------------------
        # Convert to string
        # -----------------------

        if isinstance(result, dict):
            report = "\n".join(
                f"{k}: {v}" for k, v in result.items()
            )

        elif isinstance(result, (list, tuple)):
            report = "\n".join(map(str, result))

        else:
            report = str(result)

        # -----------------------
        # Extract ATS Score
        # -----------------------

        score = 0

        patterns = [
            r"ATS\s*Score\s*[:\-]?\s*(\d{1,3})",
            r"Score\s*[:\-]?\s*(\d{1,3})",
            r"(\d{1,3})\s*/\s*100"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                report,
                re.IGNORECASE
            )

            if match:

                score = min(
                    int(match.group(1)),
                    100
                )

                break

        # -----------------------
        # Remove ATS Score line
        # -----------------------

        report = re.sub(
            r"ATS\s*Score\s*[:\-]?\s*\d{1,3}\s*/?\s*100?",
            "",
            report,
            flags=re.IGNORECASE
        )

        report = report.strip()

        # -----------------------
        # UI
        # -----------------------

        st.success("✅ Analysis Completed")

        col1, col2 = st.columns([1, 3])

        with col1:
            st.metric(
                "ATS Score",
                f"{score}%"
            )

        with col2:
            st.progress(score / 100)

        st.divider()

        st.subheader("📄 ATS Report")

        st.markdown(report)
# ==========================================================
# SKILL GROWTH
# ==========================================================

elif st.session_state.page == "Skill Growth":

    st.title("📈 AI Skill Growth Roadmap")
    st.caption("Upload your resume and get a personalized AI career roadmap.")

    resume = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        key="skill_resume"
    )

    if resume is not None:

        # Save uploaded PDF
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:

            tmp.write(resume.read())
            pdf_path = tmp.name

        # Read resume text
        resume_text = rag.read_pdf(pdf_path)

        # Generate roadmap
        with st.spinner("Generating your personalized roadmap..."):
            result = skill_growth(resume_text)

        st.success("✅ Skill Growth Roadmap Generated")

        st.divider()

        with st.container(border=True):
            st.markdown(result)

        st.divider()

        st.info(
            """
### 💡 Tips

- Complete one project after every major topic.
- Keep updating your GitHub portfolio.
- Practice interview questions weekly.
- Learn one new technology every month.
- Build an ATS-friendly resume after learning new skills.
            """
        )
# ==========================================================
# JD MATCH
# ==========================================================
elif st.session_state.page == "JD Match":

    st.title("🎯 Resume vs Job Description")

    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf"],
        key="jd_resume"
    )

    jd = st.text_area(
        "Paste Job Description",
        height=250
    )

    if st.button("Analyze Match"):

        if resume is None:
            st.warning("Upload your resume.")
            st.stop()

        if not jd.strip():
            st.warning("Paste a Job Description.")
            st.stop()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(resume.read())
            pdf_path = tmp.name

        resume_text = rag.read_pdf(pdf_path)

        with st.spinner("Comparing Resume..."):

            result = jd_match(
                resume_text,
                jd
            )

        st.markdown(result)
# ==========================================================
# OCR
# ==========================================================

# ==========================================================
# OCR
# ==========================================================
elif st.session_state.page == "OCR":

    st.title("🖼 AI OCR")

    st.caption(
        "Extract text from images or ask questions."
    )

    image = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"]
    )

    question = st.text_input(
        "Ask anything about the image (Optional)"
    )

    if image:

        st.image(
            image,
            use_container_width=True
        )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".png"
        ) as tmp:

            tmp.write(image.read())
            path = tmp.name

        if st.button(
            "Extract Text",
            use_container_width=True
        ):

            with st.spinner("Reading Image..."):

                text = ocr.extract_text(path)

            st.subheader("📄 Extracted Text")

            st.text_area(
                "",
                text,
                height=250
            )

        if st.button(
            "Ask AI",
            use_container_width=True,
            disabled=not question.strip()
        ):

            with st.spinner("🤖 Thinking..."):

                answer = ocr.ask(
                    path,
                    question
                )

            st.success(answer)
# ==========================================================
# WEB SEARCH
# ==========================================================

# ==========================================================
# WEB SEARCH
# ==========================================================
elif st.session_state.page == "Web Search":

    # ---------- New CSS ----------
    st.markdown("""
    <style>

    /* Page Title */
    .web-title {

        font-size: 36px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;

    }


    .web-subtitle {

        text-align:center;
        color:#777;
        font-size:17px;
        margin-bottom:25px;

    }


    /* Search Box */

    .stTextInput input {

        height:60px;
        border-radius:25px;
        border:2px solid #ddd;
        padding-left:20px;
        font-size:16px;

    }


    /* Button */

    .stButton button {

        border-radius:25px;
        height:45px;
        background:#2563eb;
        color:white;
        font-size:16px;
        font-weight:600;

    }


    .stButton button:hover {

        background:#1e40af;
        color:white;

    }



    /* Answer Box */

    .answer-box {

        background:#f1f5f9;

        padding:20px;

        border-radius:18px;

        margin-top:20px;

        font-size:17px;

        line-height:1.6;

        color:#111827;

        border:1px solid #e5e7eb;

        white-space:normal;

        word-wrap:break-word;

    }



    /* Remove extra markdown gaps */

    .answer-box p {

        display:inline;

    }


    .answer-box a {

        color:#2563eb;

    }


    </style>

    """, unsafe_allow_html=True)



    # ---------- Header ----------

    st.markdown(
        """
        <div class="web-title">
        🌐 AI Web Search
        </div>

        <div class="web-subtitle">
        Search anything and get AI generated answers
        </div>

        """,
        unsafe_allow_html=True
    )



    query = st.text_input(
        "",
        placeholder="Search here..."
    )


    if st.button(
    "🔍 Search",
    use_container_width=True
):

     if query:

        with st.spinner("Searching..."):

            result = web.search(query)


        st.markdown(
            "## 🤖 Search Results"
        )


        if result:


            formatted_result = ""


            for item in result:


                title = item.get(
                    "title",
                    "No title"
                )


                url = item.get(
                    "href",
                    ""
                )


                body = item.get(
                    "body",
                    ""
                )


                formatted_result += f"""

### {title}

🔗 {url}

{body}


"""


            st.markdown(
                formatted_result
            )


        else:

            st.warning(
                "No results found"
            )


    else:

        st.warning(
            "Enter search query"
        )
# ==========================================================
# SETTINGS
# ==========================================================

# ==========================================================
# SETTINGS
# ==========================================================

elif st.session_state.page == "Settings":

    st.title("⚙️ Settings")

    st.subheader("Profile")

    st.text_input(
        "Username",
        value=st.session_state.user,
        disabled=True
    )

    st.divider()

    st.subheader("Application")

    dark = st.toggle(
        "Dark Theme",
        value=True
    )

    memory_toggle = st.toggle(
        "Enable Conversation Memory",
        value=True
    )

    notifications = st.toggle(
        "Notifications",
        value=True
    )

    st.divider()

    st.subheader("Danger Zone")

    if st.button(
        "🗑 Clear Chat History",
        use_container_width=True
    ):

        clear_chat(
            st.session_state.user
        )

        st.success(
            "Chat History Cleared."
        )

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()
