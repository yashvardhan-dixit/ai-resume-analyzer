# AI Resume Analyzer 🤖

A powerful, AI-driven resume analysis tool that provides instant feedback on your resume's strengths, weaknesses, and match with job descriptions.

## Features

- 📄 **Multi-format Support**: PDF, DOCX, DOC, and TXT files
- 🎯 **Job Description Matching**: Compare your resume against job descriptions
- 🛠️ **Skill Extraction**: Automatically identify technical skills
- 📊 **Experience Analysis**: Detect years of experience
- 🎓 **Education Recognition**: Extract educational background
- 💡 **Smart Recommendations**: Get personalized improvement suggestions
- 📱 **Responsive Design**: Works on all devices

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/resume-analyzer.git
   cd resume-analyzer
2. **Create virtual environment***:
    ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install dependencies**:
    ```bash
   pip install -r requirements.txt
4. **Download spaCy model**:
   ```bash
   python -m spacy download en_core_web_sm
