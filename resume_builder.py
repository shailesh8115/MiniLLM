import streamlit as st

from rag import rag
from resume import extract_resume_data

# ======================================
# RESUME BUILDER
# ======================================

import streamlit as st

def resume_builder():
    st.title("Resume Builder")

    st.caption(
        "Build an ATS-friendly resume using AI."
    )

    st.divider()

    # -----------------------------
    # Upload Resume
    # -----------------------------

    uploaded_resume = st.file_uploader(
        "📄 Upload Existing Resume",
        type=["pdf"]
    )

    auto = {}

    if uploaded_resume:

        with st.spinner("Reading Resume..."):

            try:

                resume_text = rag.read_pdf(
                    uploaded_resume
                )

                auto = extract_resume_data(
                    resume_text
                )

                st.success(
                    "Resume Parsed Successfully"
                )

            except Exception as e:

                st.error(e)

    # -----------------------------
    # Template Selection
    # -----------------------------

    st.subheader("🎨 Resume Template")

    templates = {
        "Modern": "templates/modern.png",
        "Professional": "templates/professional.png",
        "Harvard": "templates/harvard.png",
        "Executive": "templates/executive.png",
        "Minimal": "templates/minimal.png"
    }

    template = st.selectbox(
        "Choose Template",
        list(templates.keys())
    )

    if template in templates:

        try:

            st.image(
                templates[template],
                width=300
            )

        except:

            st.info(
                "Template Preview Not Available"
            )

    st.divider()

    # -----------------------------
    # Personal Information
    # -----------------------------

    st.subheader("👤 Personal Information")

    left, right = st.columns(2)

    with left:

        name = st.text_input(
            "Full Name",
            auto.get("name", "")
        )

        email = st.text_input(
            "Email",
            auto.get("email", "")
        )

        phone = st.text_input(
            "Phone",
            auto.get("phone", "")
        )

    with right:

        role = st.text_input(
            "Target Role",
            auto.get(
                "role",
                "AI Engineer"
            )
        )

        linkedin = st.text_input(
            "LinkedIn"
        )

        github = st.text_input(
            "GitHub"
        )

    st.divider()

    # -----------------------------
    # Resume Completion
    # -----------------------------

    fields = [
        name,
        email,
        phone,
        role,
        linkedin,
        github
    ]

    completed = sum(
        bool(i.strip())
        for i in fields
    )

    progress = completed / len(fields)

    st.subheader("📊 Resume Completion")

    st.progress(progress)

    st.write(
        f"{int(progress*100)}% Complete"
    )

    if progress < 0.40:

        st.warning(
            "Complete more details."
        )

    elif progress < 0.80:

        st.info(
            "Looking Good."
        )

    else:

        st.success(
            "Almost Ready!"
        )

    st.divider()

    return {

        "template": template,

        "name": name,

        "email": email,

        "phone": phone,

        "role": role,

        "linkedin": linkedin,

        "github": github

    }