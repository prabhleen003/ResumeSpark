import streamlit as st
from streamlit_extras import add_vertical_space as avs
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
from PIL import Image
import matplotlib.pyplot as plt

load_dotenv()  # Load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input)
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

#Convert PDF content to Text format
def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            text += str(page.extract_text())
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

# Function to create a doughnut chart
def create_doughnut_chart(percentage):
    fig, ax = plt.subplots(figsize=(6, 6))
    sizes = [percentage, 100 - percentage]
    colors = ['#4CAF50', '#E0E0E0']
    explode = (0.1, 0)  
    ax.pie(sizes, colors=colors, startangle=90, explode=explode, wedgeprops=dict(width=0.3))
    ax.text(0, 0, f'{percentage}%', ha='center', va='center', fontsize=24, fontweight='bold')
    ax.set_title("Match Percentage", fontsize=16)
    ax.axis('equal')  
    return fig


# Streamlit UI
st.set_page_config(page_title="Resume ATS Tracker", layout="wide")


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    .stApp {
        background-color: #34CD8C;
        color: black;
        font-family: 'Roboto', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        color: black;
        font-family: 'Roboto', sans-serif;
    }
    p, div, span {
        color: black;
        font-family: 'Roboto', sans-serif;
    }
    .stImage {
        margin: auto;
        display: block;
        margin: 12px 12px;
        border-radius: 15px;
    }
    .stButton>button {
        background-color: #006400;
        color: #ffffff !important;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #004d00;
    }
    .header-title {
        text-align: center;
        font-weight: 700;
        font-size: 2.5em;
    }
    .sub-header {
        text-align: center;
        font-weight: 400;
        font-size: 1.5em;
    }
    .description {
        text-align: justify;
        font-weight: 300;
        font-size: 1.2em;
    }
    .offerings {
        font-weight: 300;
        font-size: 1.2em;
    }
    .faq-container {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .faq-question {
        font-weight: 400;
        font-size: 1.2em;
    }
    .faq-answer {
        font-weight: 300;
        font-size: 1.2em;
        margin-bottom: 10px;
    }
    .stTextInput > div, .stTextArea > div {
        background-color: #d4edda;  /* Light green background */
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

avs.add_vertical_space(4)
col1, col2 = st.columns([3, 2])
with col1:
    st.title("CareerCraft")
    st.header("Navigate the Job Market with Confidence!")
    st.markdown("""
                <p class='description'>
                Introducing CareerCraft, an ATS-Optimized Resume Analyzer your ultimate solution 
                for optimizing job applications and accelerating career growth. Our innovative platform 
                leverages advanced ATS technology to provide job seekers with valuable insights into their resumes' 
                compatibility with job descriptions. From resume optimization and skill enhancement to career progression guidance, 
                CareerCraft empowers users to stand out in today's competitive job market. Streamline your job application process, 
                enhance your skills, and navigate your career path with confidence. Join CareerCraft today and unlock new opportunities 
                for professional success!
                </p>
                """, unsafe_allow_html=True)
with col2:
    st.image('https://cdn.dribbble.com/userupload/12500996/file/original-b458fe398a6d7f4e9999ce66ec856ff9.gif', use_column_width=True)

avs.add_vertical_space(10)

col1, col2 = st.columns([3, 2])
with col2:
    st.header("Wide Range of Offerings")
    st.markdown("""
                <ul class='offerings'>
                    <li>ATS-Optimized Resume Analysis</li>
                    <li>Resume Optimization</li>
                    <li>Skill Enhancement</li>
                    <li>Career Progression Guidance</li>
                    <li>Tailored Profile Summaries</li>
                    <li>Streamlined Application Process</li>
                    <li>Personalized Recommendations</li>
                    <li>Efficient Career Navigation</li>
                </ul>
                """, unsafe_allow_html=True)
with col1:
    img1 = Image.open("images/icon1.png")
    st.image(img1, use_column_width=True, caption="Optimize Your Resume")

avs.add_vertical_space(10)

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("<h1 class='header-title'>Embark on Your Career Adventure</h1>", unsafe_allow_html=True)
    jd = st.text_area("Paste the Job Description")
    uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")
    submit = st.button("Submit")
    if submit:
        if uploaded_file is not None and jd:
            text = input_pdf_text(uploaded_file)
            input_prompt = f"""
            As an experienced ATS (Applicant Tracking System), proficient in the technical domain encompassing Software Engineering, Data Science, Data Analysis, Big Data Engineering, Web Developer, Mobile App Developer, DevOps Engineer, Machine Learning Engineer, Cybersecurity Analyst, Cloud Solutions Architect, Database Administrator, Network Engineer, AI Engineer, Systems Analyst, Full Stack Developer, UI/UX Designer, IT Project Manager, and additional specialized areas, your objective is to meticulously assess resumes against provided job descriptions. In a fiercely competitive job market, your expertise is crucial in offering top-notch guidance for resume enhancement. Assign precise matching percentages based on the JD (Job Description) and meticulously identify any missing keywords with utmost accuracy.
            resume: {text}
            description: {jd}
            I want the response in the following structure:
            The first line indicates the percentage match with the job description (JD).
            The second line presents a list of missing keywords.
            The third section provides a profile summary.
            Mention the title for all the three sections.
            While generating the response put some space to separate all the three sections.
            """
            response = get_gemini_response(input_prompt)
            if response:
                st.subheader("Analysis Result")
                left_col, right_col = st.columns([2, 1])
                with left_col:
                    st.markdown(response)
                match_percentage = 0 
                try:
                    match_percentage = int(response.split('\n')[0].split(' ')[-1].strip('%'))
                except:
                    st.error("Failed to extract match percentage from the response.")
            
                with right_col:
                    fig = create_doughnut_chart(match_percentage)
                    st.pyplot(fig)
        else:
            st.error("Please provide both the job description and upload your resume.")
with col2:
    img2 = Image.open("images/icon2.png")
    st.image(img2, use_column_width=True, caption="Career Guidance")


avs.add_vertical_space(10)


col1, col2 = st.columns([2, 3])
with col2:
    st.markdown("<h1 class='sub-header'>FAQ</h1>", unsafe_allow_html=True)
    st.markdown("""
                <div class="faq-container">
                    <p class='faq-question'>Question: How does CareerCraft analyze resumes and job descriptions?</p>
                    <p class='faq-answer'>Answer: CareerCraft uses advanced algorithms to analyze resumes and job descriptions, identifying key keywords and assessing compatibility between the two.</p>
                </div>
                <div class="faq-container">
                    <p class='faq-question'>Question: Is CareerCraft suitable for both entry-level and experienced professionals?</p>
                    <p class='faq-answer'>Answer: Absolutely! CareerCraft caters to job seekers at all career stages, offering tailored insights and guidance to enhance their resumes and advance their careers.</p>
                </div>
                <div class="faq-container">
                    <p class='faq-question'>Question: Can CareerCraft suggest improvements for my resume?</p>
                    <p class='faq-answer'>Answer: Yes, CareerCraft provides personalized recommendations to optimize your resume for specific job openings, including suggestions for missing keywords and alignment with desired job roles.</p>
                </div>
                """, unsafe_allow_html=True)
with col1:
    img3 = Image.open("images/icon3.png")
    st.image(img3, use_column_width=True, caption="Advanced Analysis")

avs.add_vertical_space(10)
