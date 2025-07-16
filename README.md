# 🚀 ResumeSpark: ATS-Optimized Resume Analyzer Using Gemini Model

**ResumeSpark** is a smart, AI-powered resume analysis tool built with Google Generative AI. It helps job seekers evaluate how well their resumes align with specific job descriptions. Through a responsive Streamlit web interface, users receive actionable insights to improve their ATS (Applicant Tracking System) match score and overall resume quality.
*link* https://resumespark-crje3lazswm4bpbsd7frmg.streamlit.app/

---

## ✨ Features

- 📄 Upload resumes in PDF format  
- 📝 Enter any job description text  
- 🤖 Analyze with Google Generative AI (Gemini)  
- 📊 View:
  - ✅ Match Percentage
  - 🔍 Missing Keywords
  - 🧠 Profile Summary  
- 🎨 Clean and intuitive Streamlit UI  

---

## 🛠️ Tech Stack

| Tool/Library             | Purpose                                   |
|--------------------------|-------------------------------------------|
| `Python`                 | Core language                             |
| `Streamlit`              | Web app UI                                |
| `google-generativeai`   | Resume analysis via Gemini model          |
| `PyPDF2`                 | Extract text from PDF resumes             |
| `Pillow (PIL)`           | Image handling in Python                  |
| `python-dotenv`          | Manage secrets via `.env` file            |

---

## ⚙️ How It Works

1. 🔑 Loads API key from `.env` using `dotenv`.  
2. 📤 Extracts text from the uploaded PDF using `PyPDF2`.  
3. 🧠 Sends the resume and job description to Gemini model via `google-generativeai`.  
4. ⏳ Displays a loading spinner during analysis.  
5. 📈 Returns:
   - Resume-to-job match %
   - Missing keywords
   - Personalized profile summary

---

## 🧑‍💻 Getting Started

### 📁 1. Clone the Repository

```bash
git clone https://github.com/prabhleen003/ResumeSpark.git
cd resume-spark
```

### 📦 2. Install Dependencies

```bash
pip install streamlit python-dotenv google-generativeai pypdf2 pillow
```

### 🔐 3. Add Your API Key

Create a `.env` file in the project root and add:

```env
GOOGLE_API_KEY=your_api_key_here
```

### ▶️ 4. Run the App

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
resume-spark/
├── app.py               # Main Streamlit app
├── .env                 # API key file (not committed)
├── README.md            # Project documentation
└── requirements.txt     # Optional dependency file
```

---

## 🧠 Usage Guide

1. 🚀 Launch the app with `streamlit run app.py`  
2. 📄 Upload your resume (PDF only)  
3. 📝 Paste your job description  
4. ✅ Click "Submit"  
5. 📊 View:
   - Compatibility score
   - Missing skills/keywords
   - AI-generated summary  
6. 🧾 Improve your resume based on the feedback  

---


## 🌟 Future Scope

- 🔐 Add user login and resume history  
- 📤 Export feedback to PDF  
- 🌐 Support for `.docx` and `.txt` formats  
- 💬 Multi-language resume support  
- 📈 Resume scoring over time  


