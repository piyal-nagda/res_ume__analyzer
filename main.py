from utility import *
from streamlit_option_menu import option_menu

# --- PAGE SETUP ---
# Initialize streamlit app
page_title = "Resume Analyzer"
page_icon = "📝"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="centered")

# Display the lottie file
display_lottiefile("resume.json")

if "response" not in st.session_state:
    st.session_state.response = ''

# --- SIDEBAR SETUP ---
# Configure the API key
st.sidebar.title("Config️uration Options")
api_key = sidebar_api_key_configuration()

# ---- MAIN PAGE ----
st.title("AI Powered Resume Analyzer 🤖")
st.write("***Unlock Your Potential: Resume Analyzer for Perfect Job Matches!***")
st.write("***This app analyzes your resume, compares it to the provided job description and provides an "
         "score thus elevating your chances of career success. All powered by AI.***")
st.subheader("Job Description")
jd = st.text_area("Insert Job Description", placeholder="Inset Job Description",
                  disabled=not st.session_state.prompt_activation, label_visibility="collapsed")
st.header("Upload Resume")
uploaded_file = st.file_uploader("Upload the file", type=["pdf"],
                                 disabled=not st.session_state.prompt_activation, label_visibility="collapsed")
submit = st.button("Submit", type="primary", disabled=not uploaded_file)
if submit:
    if uploaded_file is not None:
        with st.spinner("Analyzing ..."):
            resume_text = get_pdf_text(uploaded_file)
            st.session_state.response = get_gemini_response(resume_text, jd, api_key)


# ---- NAVIGATION MENU -----
selection = option_menu(
    menu_title=None,
    options=["Analyze", "About"],
    icons=["bi-boxes", "app"],  # https://icons.getbootstrap.com
    orientation="horizontal")

# If selected menu option is "Analyze"
if selection == 'Analyze':
    st.write(st.session_state.response)

# If selected menu option is "About"
if selection == "About":
    with st.expander("About this App"):
        st.markdown(''' This is an AI Powered Resume Analyzer app. It compares your resume to provided job description 
        and suggest improvement. It has following functionality:

    - Provides resume Matching percentage with job description
    - Missing Keywords
    - Tips for improving resume
    - Resume Rating

        ''')
    with st.expander("Which Large Language models are supported by this App?"):
        st.markdown(''' This app supports following multimodal:

    * Google -- gemini-1.5-pro-latest

        ''')
    with st.expander("Where to get the source code of this app?"):
        st.markdown(''' Source code is available at:
    -  ....
        ''')

    with st.expander("Whom to contact regarding this app?"):
        st.markdown(''' Contact [Priyal Nagda](priyalmn0703@gmail.com)
        ''')
