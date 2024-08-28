import google.generativeai as genai
from streamlit_lottie import st_lottie
import streamlit as st
from pypdf import PdfReader
import json

input_prompt_resume = """
You possess an advanced expertise as an Application Tracking System and proficient in technology industry,
encompassing software engineering, data science, dev ops, web development and big data.

Your objective is to assess resumes in alignment with the provided job description.

Given the highly competitive job market, your role involves offering top-notch guidance to enhance resume effectively.

Assign the percentage matching, give rating to the resume out of 10, give additional tips to resume based on JD 
and also give missing keywords with high accuracy.

**Resume**: {text}
**Job Description**: {jd}

Give the response in markdown form and make it as attractive as possible and use emojis wherever needed.

**Match Percentage** : %

**Missing Keywords** : ""

**Profile Summary** : ""

**Additional Tips** : ""

**Resume Rating** : 

Each of the above should be in separate lines. Provide missing keywords in bullet points
"""

if "prompt_activation" not in st.session_state:
    st.session_state.prompt_activation = False


# Function for API configuration at sidebar
def sidebar_api_key_configuration():
    st.sidebar.subheader("API Keys")
    api_key = st.sidebar.text_input("Enter your API Key 🗝️", type="password",
                                    help='Get API Key from: https://aistudio.google.com/app/apikey')
    if api_key == '':
        st.sidebar.warning('Enter the API Key 🗝️')
        st.session_state.prompt_activation = False
    elif api_key.startswith('AI') and (len(api_key) == 39):
        st.sidebar.success('Lets Proceed!', icon='️👉')
        st.session_state.prompt_activation = True
    else:
        st.sidebar.warning('Please enter the correct API Key 🗝️!', icon='⚠️')
        st.session_state.prompt_activation = False
    return api_key


# Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# Function to load and display the lottie file
def display_lottiefile(filename):
    # Load the lottie file
    with open(filename, "r") as f:
        lottie_file = json.load(f)
    st_lottie(lottie_file, speed=1, reverse=False, loop=True, quality="high", height=150, width=300, key=None)


# Function to get the list of available gemini models
def get_gemini_model_list():
    model_list = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_list.append(m.name)
    return model_list


# Function to get the response from gemini model with text as the input
def get_gemini_response(input_resume, jd, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content([input_prompt_resume, jd, input_resume])
    return response.text
