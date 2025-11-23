import re
import nltk
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
from docx import Document
import textract
import string
from collections import Counter

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ResumeAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.skills_db = [
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift',
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask',
            'machine learning', 'deep learning', 'ai', 'data analysis', 'sql',
            'mongodb', 'postgresql', 'aws', 'azure', 'docker', 'kubernetes',
            'git', 'jenkins', 'ci/cd', 'rest api', 'graphql', 'agile', 'scrum'
        ]
    
    def extract_text(self, file_path):
        """Extract text from various file formats"""
        file_extension = file_path.split('.')[-1].lower()
        
        try:
            if file_extension == 'pdf':
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page in reader.pages:
                        text += page.extract_text()
                    return text
                    
            elif file_extension in ['docx', 'doc']:
                if file_extension == 'docx':
                    doc = Document(file_path)
                    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                else:
                    text = textract.process(file_path).decode('utf-8')
                return text
                
            elif file_extension == 'txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
                    
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:]', '', text)
        return text.lower().strip()
    
    def extract_skills(self, text):
        """Extract skills from resume text"""
        found_skills = []
        text_lower = text.lower()
        
        for skill in self.skills_db:
            if skill in text_lower:
                found_skills.append(skill)
        
        return list(set(found_skills))
    
    def extract_experience(self, text):
        """Extract experience information"""
        # Look for experience patterns
        experience_patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of)?\s*experience',
            r'experience\s*:\s*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)\s*in'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return max([int(match) for match in matches])
        
        return 0
    
    def extract_education(self, text):
        """Extract education information"""
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'bs', 'ms', 'mba',
            'university', 'college', 'degree', 'graduated'
        ]
        
        education = []
        sentences = nltk.sent_tokenize(text)
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in education_keywords):
                education.append(sentence.strip())
        
        return education[:3]  # Return top 3 education entries
    
    def calculate_match_score(self, resume_text, job_description):
        """Calculate match score between resume and job description"""
        if not job_description.strip():
            return 75  # Default score if no JD provided
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
        
        # Calculate cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        match_score = cosine_sim[0][0] * 100
        
        return round(match_score, 2)
    
    def analyze_resume(self, file_path, job_description=""):
        """Main analysis function"""
        # Extract text
        raw_text = self.extract_text(file_path)
        cleaned_text = self.preprocess_text(raw_text)
        
        # Perform analysis
        skills = self.extract_skills(cleaned_text)
        experience = self.extract_experience(cleaned_text)
        education = self.extract_education(cleaned_text)
        match_score = self.calculate_match_score(cleaned_text, job_description)
        
        # Calculate word count
        word_count = len(cleaned_text.split())
        
        # Generate recommendations
        recommendations = self.generate_recommendations(skills, experience, word_count, job_description)
        
        return {
            'success': True,
            'analysis': {
                'skills_found': skills,
                'experience_years': experience,
                'education': education,
                'match_score': match_score,
                'word_count': word_count,
                'recommendations': recommendations
            },
            'metadata': {
                'skills_count': len(skills),
                'education_count': len(education)
            }
        }
    
    def generate_recommendations(self, skills, experience, word_count, job_description):
        """Generate personalized recommendations"""
        recommendations = []
        
        # Skill-based recommendations
        if len(skills) < 5:
            recommendations.append("Consider adding more technical skills to your resume")
        
        # Experience recommendations
        if experience == 0:
            recommendations.append("Highlight any projects or internships to demonstrate practical experience")
        
        # Length recommendations
        if word_count < 200:
            recommendations.append("Your resume seems brief. Consider adding more details about your projects and achievements")
        elif word_count > 800:
            recommendations.append("Your resume might be too long. Consider condensing to the most relevant information")
        
        # Job description specific recommendations
        if job_description:
            jd_skills = self.extract_skills(job_description.lower())
            missing_skills = set(jd_skills) - set(skills)
            if missing_skills:
                recommendations.append(f"Consider adding these skills mentioned in the job description: {', '.join(list(missing_skills)[:3])}")
        
        return recommendations if recommendations else ["Your resume looks good! Make sure to tailor it for each specific job application."]
