import streamlit as st
import time

from database import (
    login,
    register_user
)

# ==========================================================
# SESSION STATE
# ==========================================================

def init_session():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user" not in st.session_state:
        st.session_state.user = None

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    if "messages" not in st.session_state:
        st.session_state.messages = []


# ==========================================================
# CUSTOM CSS
# ==========================================================

def load_css():

    st.markdown(
        """
<style>

.main{
    background:#0E1117;
}

.block-container{
    padding-top:2rem;
}

.login-card{
    background:#161B22;
    padding:35px;
    border-radius:20px;
}

.stButton>button{
    width:100%;
    border-radius:12px;
    height:45px;
    font-weight:bold;
}

h1{
    text-align:center;
}

</style>
""",
        unsafe_allow_html=True
    )


# ==========================================================
# LOGIN PAGE
# ==========================================================

def login_page():

    init_session()

    load_css()

    left, center, right = st.columns([1,2,1])

    with center:

        st.markdown("# 🤖 MiniLLM")

        st.caption(
            "AI Resume Builder • ATS • OCR • RAG Chat"
        )

        login_tab, signup_tab = st.tabs(
            [
                "🔐 Login",
                "📝 Sign Up"
            ]
        )

        # ==================================================
        # LOGIN
        # ==================================================

        with login_tab:

            username = st.text_input(
                "Username",
                placeholder="Enter Username",
                key="login_user"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter Password",
                key="login_pass"
            )

            remember = st.checkbox(
                "Remember Me"
            )

            if st.button(
                "🚀 Login",
                use_container_width=True
            ):

                if username == "" or password == "":

                    st.warning(
                        "Please fill all fields."
                    )

                elif login(username, password):

                    st.session_state.logged_in = True
                    st.session_state.user = username
                    st.session_state.page = "Dashboard"

                    st.success(
                        "Login Successful"
                    )

                    time.sleep(1)

                    st.rerun()

                else:

                    st.error(
                        "Invalid Username or Password"
                    )

        # ==================================================
        # SIGNUP
        # ==================================================

        with signup_tab:

            new_user = st.text_input(
                "Username",
                key="signup_user"
            )

            email = st.text_input(
                "Email",
                key="signup_email"
            )

            new_pass = st.text_input(
                "Password",
                type="password",
                key="signup_pass"
            )

            confirm = st.text_input(
                "Confirm Password",
                type="password",
                key="signup_confirm"
            )

            if st.button(
                "📝 Create Account",
                use_container_width=True
            ):

                if "" in [
                    new_user,
                    email,
                    new_pass,
                    confirm
                ]:

                    st.warning(
                        "Please fill all fields."
                    )

                elif new_pass != confirm:

                    st.error(
                        "Passwords do not match."
                    )

                else:

                    ok = register_user(
                        new_user,
                        email,
                        new_pass
                    )

                    if ok:

                        st.success(
                            "Account created successfully."
                        )

                        st.info(
                            "Please login."
                        )

                    else:

                        st.error(
                            "Username or Email already exists."
                        )


# ==========================================================
# LOGOUT
# ==========================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.page = "Dashboard"

    if "messages" in st.session_state:
        st.session_state.messages = []

    st.rerun()