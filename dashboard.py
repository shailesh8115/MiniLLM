import streamlit as st

from database import (
    dashboard_stats,
    load_chat
)

from rag import rag


# ==========================================================
# HOME PAGE
# ==========================================================

def home_page():

    stats = dashboard_stats(
        st.session_state.user
    )

    st.title("🤖 MiniLLM AI Assistant")

    st.markdown(
        f"## 👋 Welcome back, **{st.session_state.user}**"
    )

    st.caption(
        "Your Personal AI Assistant powered by RAG, OCR and LLM."
    )

    st.divider()

    # ==================================================
    # DASHBOARD CARDS
    # ==================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💬 Chats",
        stats["chats"]
    )

    c2.metric(
        "📄 PDFs",
        rag.count()
    )

    c3.metric(
        "📝 Resumes",
        stats["resumes"]
    )

    c4.metric(
        "🔍 Searches",
        stats["searches"]
    )

    st.divider()

    # ==================================================
    # QUICK ACTIONS
    # ==================================================

    st.subheader("🚀 Quick Actions")

    a, b, c = st.columns(3)

    if a.button(
        "💬 AI Chat",
        use_container_width=True
    ):
        st.session_state.page = "AI Chat"
        st.rerun()

    if b.button(
        "📝 Resume Builder",
        use_container_width=True
    ):
        st.session_state.page = "Resume Builder"
        st.rerun()

    if c.button(
        "📊 ATS Checker",
        use_container_width=True
    ):
        st.session_state.page = "ATS Checker"
        st.rerun()

    d, e, f = st.columns(3)

    if d.button(
        "📈 Skill Growth",
        use_container_width=True
    ):
        st.session_state.page = "Skill Growth"
        st.rerun()

    if e.button(
        "🖼 OCR",
        use_container_width=True
    ):
        st.session_state.page = "OCR"
        st.rerun()

    if f.button(
        "🌐 Web Search",
        use_container_width=True
    ):
        st.session_state.page = "Web Search"
        st.rerun()

    st.divider()
        # ==================================================
    # AI FEATURES
    # ==================================================

    st.subheader("✨ AI Features")

    col1, col2 = st.columns(2)

    with col1:

        st.info("""
### 💬 AI Chat

✔ Chat with your PDF documents

✔ RAG Powered

✔ Conversation Memory

✔ Multi PDF Support
""")

        st.info("""
### 📝 Resume Builder

✔ AI Resume Builder

✔ ATS Friendly Resume

✔ DOCX Export

✔ PDF Export
""")

        st.info("""
### 🎯 JD Match

✔ Compare Resume

✔ Job Description Matching

✔ Missing Skills

✔ Suggestions
""")

    with col2:

        st.info("""
### 📊 ATS Checker

✔ ATS Score

✔ Keyword Analysis

✔ Resume Improvements

✔ AI Suggestions
""")

        st.info("""
### 🖼 OCR

✔ Image to Text

✔ PDF OCR

✔ Ask Questions from Images

✔ AI Extraction
""")

        st.info("""
### 🌐 Web Search

✔ Internet Search

✔ AI Summary

✔ Latest Information

✔ Save Search History
""")

    st.divider()

    # ==================================================
    # RECENT ACTIVITY
    # ==================================================

    st.subheader("📈 Recent Activity")

    history = load_chat(
        st.session_state.user
    )

    if history:

        for question, answer in history[-5:]:

            with st.expander(f"💬 {question}"):

                st.write(answer)

    else:

        st.info("No recent chats available.")

    st.divider()

    # ==================================================
    # QUICK TIPS
    # ==================================================

    st.subheader("💡 Tips")

    tip1, tip2, tip3 = st.columns(3)

    with tip1:

        st.success("""
### 📄 Upload PDFs

Upload multiple PDF files.

MiniLLM indexes them automatically for AI Chat.
""")

    with tip2:

        st.success("""
### 🤖 Ask Questions

Use AI Chat to ask anything from your uploaded documents.
""")

    with tip3:

        st.success("""
### 📝 Resume Builder

Generate professional ATS-friendly resumes with one click.
""")

    st.divider()

    # ==================================================
    # PROJECT STATUS
    # ==================================================

    st.subheader("🚀 MiniLLM Status")

    status1, status2, status3 = st.columns(3)

    status1.metric(
        "Database",
        "✅ Online"
    )

    status2.metric(
        "AI Model",
        "✅ Ready"
    )

    status3.metric(
        "Documents",
        rag.count()
    )

    st.divider()

    # ==================================================
    # FOOTER
    # ==================================================

    st.markdown(
        """
---
<center>

### 🤖 MiniLLM AI Assistant

Made with ❤️ using

**Streamlit • Python • FAISS • Llama • RAG • SQLite**

Version **1.0.0**

</center>
""",
        unsafe_allow_html=True
    )