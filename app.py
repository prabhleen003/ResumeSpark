import streamlit as st
from streamlit_extras import add_vertical_space as avs
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

load_dotenv()

# Configure API with better error handling
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("⚠ Google API Key not found. Please set GOOGLE_API_KEY in your .env file")
        st.stop()
    
    genai.configure(api_key=api_key)
    # st.success("✅ API configured successfully")
except Exception as e:
    # st.error(f"❌ API configuration failed: {e}")
    st.stop()

def get_gemini_response(input_text):
    """Enhanced function with better error handling and debugging"""
    try:
        # st.info("🔄 Connecting to Gemini API...")
        
        # Try different models if one fails
        models_to_try = [ 'gemini-1.5-flash', 'gemini-1.5-pro']
        
        for model_name in models_to_try:
            try:
                # st.info(f"🧠 Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                # Add generation config for better control
                generation_config = {
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
                
                response = model.generate_content(
                    input_text,
                    generation_config=generation_config
                )
                
                if response and response.text:
                    st.success(f"✅ Response generated successfully  ")
                    return response.text
                else:
                    st.warning(f"⚠ Empty response ")
                    
            except Exception as model_error:
                # st.warning(f"❌ Model {model_name} failed: {str(model_error)}")
                continue
        
        st.error("❌ failed. Please check your API key and quota and Try Again.")
        return None
        
    except Exception as e:
        st.error(f"❌ Critical error in API call: {str(e)}")
        st.error("🔍 Debug info: Check if your API key is valid and you have quota remaining")
        return None

def input_pdf_text(uploaded_file):
    """Enhanced PDF text extraction with better error handling"""
    try:
        # st.info("📄 Extracting text from PDF...")
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        if text.strip():
            st.success(f"✅ Successfully extracted text  from PDF")
            return text
        else:
            st.error("❌ No text found in PDF. Please ensure it's not an image-based PDF.")
            return None
            
    except Exception as e:
        st.error(f"❌ Error reading PDF file: {str(e)}")
        st.error("💡 Try: 1) Re-saving PDF 2) Using a different PDF 3) Checking file isn't corrupted")
        return None

def create_modern_chart(percentage):
    """Create a modern donut chart for match percentage"""
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a0a')
    
    # Create a modern donut chart
    sizes = [percentage, 100 - percentage]
    colors = ['#00ffff', '#1a1a1a']
    explode = (0.05, 0)
    
    wedges, texts = ax.pie(sizes, colors=colors, startangle=90, explode=explode,
                          wedgeprops=dict(width=0.4, edgecolor='#333'))
    
    # Add percentage text in center
    ax.text(0, 0, f'{percentage}%', ha='center', va='center', 
            fontsize=24, fontweight='bold', color='#00ffff')
    ax.text(0, -0.3, 'MATCH', ha='center', va='center', 
            fontsize=12, color='#888', fontweight='bold')
    
    ax.set_title("Resume Match Score", fontsize=14, color='#00ffff', pad=20)
    fig.patch.set_facecolor('#0a0a0a')
    
    return fig

# Test API connection on startup
def test_api_connection():
    """Test if API is working"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        test_response = model.generate_content("Say 'API working'")
        if test_response and test_response.text:
            return True
    except:
        return False

st.set_page_config(
    page_title="ResumeSpark - AI Resume Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean, modern CSS (same as before)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
    color: #e0e0e0;
    font-family: 'Inter', sans-serif;
}

/* Header */
.main-header {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1));
    border-radius: 20px;
    margin-bottom: 2rem;
     margin-top: -4rem;
    border: 1px solid rgba(0, 255, 255, 0.2);
}

.main-title {
    font-size: 7rem;
    font-weight: 700;
    background: linear-gradient(45deg, #00ffff, #ff00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    font-family: 'JetBrains Mono', monospace;
}

.subtitle {
    font-size: 3rem;
    color: #888;
    margin-top: 0.5rem;
}

/* Cards */
.feature-card {
    background: rgba(20, 20, 20, 0.8);
    border: 1px solid rgba(0, 255, 255, 0.3);
    border-radius: 15px;
    padding: 2rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 255, 255, 0.2);
}

.feature-card h2, .feature-card h3 {
    color: #00ffff;
    margin-bottom: 1rem;
    font-weight: 600;
}

.feature-card p {
    color: #cccccc;
    line-height: 1.6;
    margin-bottom: 1rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(45deg, #00ffff, #0099cc);
    color: #000000 !important;
    font-weight: 600;
    padding: 0.8rem 2rem;
    border-radius: 10px;
    border: none;
    font-size: 1.1rem;
    transition: all 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stButton > button:hover {
    background: linear-gradient(45deg, #0099cc, #00ffff);
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3);
}

/* Form Elements */
.stTextArea textarea, .stTextInput input {
    background: rgba(30, 30, 30, 0.9) !important;
    border: 1px solid rgba(0, 255, 255, 0.3) !important;
    border-radius: 8px !important;
    color: #e0e0e0 !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #00ffff !important;
    box-shadow: 0 0 0 1px #00ffff !important;
}

/* File Uploader */
.stFileUploader > div {
    background: rgba(30, 30, 30, 0.9) !important;
    border: 2px dashed rgba(0, 255, 255, 0.3) !important;
    border-radius: 10px !important;
    padding: 2rem !important;
}

.stFileUploader > div:hover {
    border-color: #00ffff !important;
    background: rgba(30, 30, 30, 0.95) !important;
}

/* Lists */
.feature-list {
    list-style: none;
    padding: 0;
}

.feature-list li {
    background: rgba(30, 30, 30, 0.6);
    margin: 0.5rem 0;
    padding: 1rem;
    border-left: 3px solid #00ffff;
    border-radius: 5px;
    transition: all 0.2s ease;
}

.feature-list li:hover {
    background: rgba(30, 30, 30, 0.8);
    transform: translateX(5px);
}

/* FAQ Styling - Fixed */
.faq-container {
    background: rgba(20, 20, 20, 0.8);
    border: 1px solid rgba(0, 255, 255, 0.3);
    border-radius: 15px;
    padding: 2rem;
    margin-bottom: 2rem;
}

.faq-item {
    background: rgba(30, 30, 30, 0.8);
    border: 1px solid rgba(0, 255, 255, 0.2);
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.faq-question {
    color: #00ffff;
    font-weight: 600;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
}

.faq-answer {
    color: #cccccc;
    line-height: 1.6;
    margin: 0;
}

/* Grid Layout */
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.feature-item {
    background: rgba(30, 30, 30, 0.6);
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid rgba(0, 255, 255, 0.2);
    text-align: center;
    transition: all 0.2s ease;
}

.feature-item:hover {
    border-color: #00ffff;
    background: rgba(30, 30, 30, 0.8);
}

.feature-item h4 {
    color: #00ffff;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
}

.feature-item p {
    color: #aaa;
    font-size: 0.9rem;
    margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
    .main-title {
        font-size: 2.5rem;
    }
    
    .feature-card {
        padding: 1.5rem;
    }
    
    .features-grid {
        grid-template-columns: 1fr;
    }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #1a1a1a;
}

::-webkit-scrollbar-thumb {
    background: #00ffff;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #0099cc;
}

/* Loading State */
.stSpinner {
    color: #00ffff !important;
}

/* Error Messages */
.stError {
    background: rgba(255, 0, 0, 0.1) !important;
    border: 1px solid rgba(255, 0, 0, 0.3) !important;
    border-radius: 8px !important;
    color: #ff6b6b !important;
}

/* Success Messages */
.stSuccess {
    background: rgba(0, 255, 0, 0.1) !important;
    border: 1px solid rgba(0, 255, 0, 0.3) !important;
    border-radius: 8px !important;
    color: #51cf66 !important;
}
</style>
""", unsafe_allow_html=True)

# Test API connection
if 'api_tested' not in st.session_state:
    st.session_state.api_tested = False
    if test_api_connection():
        st.session_state.api_working = True
        # st.success("🚀 API connection successful!")
    else:
        st.session_state.api_working = False
        # st.error("❌ API connection failed. Please check your setup.")

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">RESUME SPARK</h1>
    <p class="subtitle">AI-powered insights to tailor your resume for every opportunity.</p>
</div>
""", unsafe_allow_html=True)

# Introduction Section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="feature-card">
        <h2>🚀 Transform Your Career</h2>
        <p>ResumeSpark uses advanced AI to analyze your resume against job descriptions, providing actionable insights to help you land your dream job. Get detailed feedback on keyword matches, skill gaps, and optimization recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    # Main Analysis Section
    st.markdown("""
    <div class="feature-card">
    <h2>📋 Resume Analysis</h2>
    <p>Upload your resume and paste the job description to get started with AI-powered analysis.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3> Key Features</h3>
        <ul class="feature-list">
            <li>🎯 ATS Compatibility Check</li>
            <li>📊 Match Score Analysis</li>
            <li>🔍 Keyword Gap Detection</li>
            <li>💡 Optimization Tips</li>
            <li>📝 Profile Summary Generation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

avs.add_vertical_space(1)



col1, col2 = st.columns([1, 2])

with col2:
    # Job Description Input
    jd = st.text_area(
        "Job Description",
        placeholder="Paste the complete job description here...",
        height=180,
        help="Include all requirements, responsibilities, and qualifications from the job posting"
    )

    # File Upload
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type="pdf",
        help="Upload your resume in PDF format for analysis"
    )

    # Debug info
    if st.checkbox("🔧 Show Debug Info"):
        st.info(f"API Key Present: {'Yes' if os.getenv('GOOGLE_API_KEY') else 'No'}")
        st.info(f"File Uploaded: {'Yes' if uploaded_file else 'No'}")
        st.info(f"Job Description Length: {len(jd) if jd else 0} characters")

    analyze_clicked = st.button("🔍 Analyze Resume")

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>💡 Tips for Better Results</h3>
        <ul class="feature-list">
            <li>📄 Use a clean, well-formatted PDF</li>
            <li>📝 Include complete job posting text</li>
            <li>🎯 Focus on relevant keywords</li>
            <li>🔄 Re-analyze after making changes</li>
            <li>📊 Aim for 80%+ match score</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

avs.add_vertical_space(3)

# OUTSIDE col1 and col2 → Full width result area
if analyze_clicked:
    if uploaded_file is not None and jd.strip():
        # Extract text from PDF
        text = input_pdf_text(uploaded_file)

        if text:
            input_prompt = f"""
            You are an expert ATS (Applicant Tracking System) analyzer. Analyze this resume against the job description and provide detailed feedback.

            *IMPORTANT*:  Your output should be well formatted and well designed. The conent should be point to point very precise.Use well alligned bullets and headings. Use emojis to make it more engaging.
            Then provide the following sections:

            ## 📊 MATCH ANALYSIS
            - Overall compatibility score and reasoning
            - Key strengths found in the resume

            ## 🔍 MISSING KEYWORDS
            - Important keywords from job description not found in resume
            - Technical skills that should be highlighted

            ## 📈 SKILL GAPS
            - Required skills mentioned in JD but missing from resume
            - Recommended certifications or training

            ## 💡 OPTIMIZATION RECOMMENDATIONS
            - Specific changes to improve ATS compatibility
            - Suggestions for better keyword integration
            - Formatting improvements

            ## 📝 TAILORED PROFILE SUMMARY
            - A professional 2-3 sentence summary optimized for this role
            - Include relevant keywords naturally

            *Resume Content:*
            {text}

            *Job Description:*
            {jd}

            Provide actionable, specific advice to improve the resume's chances of passing ATS systems and catching recruiter attention.
            """

            response = get_gemini_response(input_prompt)

            if response:
                st.markdown("""
                <div class="feature-card">
                    <h2 style="text-align:center;">📊 Analysis Results</h2>
                </div>
                """, unsafe_allow_html=True)

                # Extract and display match percentage
                try:
                    import re
                    match_nums = re.findall(r'(\d+)%', response)
                    match_percentage = int(match_nums[0]) if match_nums else 75

                    if match_percentage >= 80:
                        color = "#00ff00"
                        status = "Excellent"
                    elif match_percentage >= 60:
                        color = "#ffff00"
                        status = "Good"
                    else:
                        color = "#ff6b6b"
                        status = "Needs Work"

                except Exception as e:
                    match_percentage = 75
                    color = "#cccccc"
                    status = "Unknown"
                    st.error(f"Error extracting match percentage: {e}")

                # Two full-width result columns
                result_col1, result_col2 = st.columns([2, 1])

                with result_col1:
                    st.markdown(f"""
                    <div class="feature-card">
                        <div style="white-space: pre-wrap; font-size: 1rem; line-height: 1.6;">
                            {response}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with result_col2:
                    st.markdown(f"""
                    <div class="feature-card" style="text-align: center;">
                        <h3>Match Score</h3>
                        <div style="font-size: 3rem; color: {color}; font-weight: bold; margin: 1rem 0;">
                            {match_percentage}%
                        </div>
                        <p style="color: #888; margin: 0;">{status}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    fig = create_modern_chart(match_percentage)
                    st.pyplot(fig)

            else:
                st.error("❌ Failed to get AI response. Please try again.")
        else:
            st.error("❌ Failed to extract text from PDF.")
    else:
        st.error("Please provide both a job description and upload your resume.")



# Features Grid
st.markdown("""
<div class="feature-card">
    <h2>🎯 Why Choose ResumeSpark?</h2>
    <div class="features-grid">
        <div class="feature-item">
            <h4>🤖 AI-Powered Analysis</h4>
            <p>Advanced machine learning algorithms analyze your resume with precision</p>
        </div>
        <div class="feature-item">
            <h4>⚡ Instant Results</h4>
            <p>Get comprehensive feedback in seconds, not hours</p>
        </div>
        <div class="feature-item">
            <h4>🎯 ATS Optimization</h4>
            <p>Ensure your resume passes Applicant Tracking Systems</p>
        </div>
        <div class="feature-item">
            <h4>📈 Career Growth</h4>
            <p>Identify skill gaps and improvement opportunities</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
avs.add_vertical_space(5)



# Footer

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🚀 Ready to Boost Your Career?</h1>
    <p class="subtitle">Join thousands of professionals who've improved their job prospects with ResumeSpark</p>
            <div style="margin-top: 1rem; font-size: 1.5rem; color: #00ffff;">
        ⭐ 🎯 📈 💼 🏆
    </div>
</div>
""", unsafe_allow_html=True)