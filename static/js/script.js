document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const resultsSection = document.getElementById('results');
    
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleFormSubmit);
    }
    
    // Check if we're on the results page and need to display results
    if (window.location.pathname === '/result') {
        displayStoredResults();
    }
});

function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData();
    const resumeFile = document.getElementById('resume').files[0];
    const jobDescription = document.getElementById('job_description').value;
    
    if (!resumeFile) {
        alert('Please select a resume file');
        return;
    }
    
    formData.append('resume', resumeFile);
    formData.append('job_description', jobDescription);
    
    // Show loading state
    const submitBtn = document.querySelector('.analyze-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');
    
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline';
    submitBtn.disabled = true;
    
    // Send AJAX request
    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Store results and redirect to results page
            localStorage.setItem('resumeAnalysis', JSON.stringify(data));
            window.location.href = '/result';
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    })
    .catch(error => {
        alert('Error: ' + error.message);
    })
    .finally(() => {
        // Reset button state
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
        submitBtn.disabled = false;
    });
}

function displayStoredResults() {
    const storedResults = localStorage.getItem('resumeAnalysis');
    const resultsContainer = document.getElementById('results');
    
    if (!storedResults) {
        resultsContainer.innerHTML = `
            <div class="result-card">
                <h3>No Results Found</h3>
                <p>Please go back and analyze a resume first.</p>
            </div>
        `;
        return;
    }
    
    const results = JSON.parse(storedResults);
    const analysis = results.analysis;
    
    // Calculate score percentage for CSS
    const scorePercent = analysis.match_score + '%';
    
    resultsContainer.innerHTML = `
        <div class="match-score">
            <div class="score-circle" style="--score-percent: ${scorePercent}">
                <span>${analysis.match_score}%</span>
            </div>
            <h3>Overall Match Score</h3>
            <p>Based on skills, experience, and job description relevance</p>
        </div>
        
        <div class="result-card">
            <h3>🛠️ Skills Found (${analysis.skills_found.length})</h3>
            <div class="skills-list">
                ${analysis.skills_found.map(skill => 
                    `<span class="skill-tag">${skill}</span>`
                ).join('')}
            </div>
        </div>
        
        <div class="result-card">
            <h3>📊 Experience</h3>
            <p><strong>Years of Experience:</strong> ${analysis.experience_years}+ years</p>
        </div>
        
        <div class="result-card">
            <h3>🎓 Education</h3>
            ${analysis.ediction.length > 0 ? 
                `<ul>${analysis.education.map(edu => `<li>${edu}</li>`).join('')}</ul>` :
                '<p>No education information detected</p>'
            }
        </div>
        
        <div class="result-card">
            <h3>📝 Resume Metrics</h3>
            <p><strong>Word Count:</strong> ${analysis.word_count} words</p>
            <p><strong>Skills Count:</strong> ${analysis.skills_found.length} unique skills</p>
        </div>
        
        <div class="result-card recommendations">
            <h3>💡 Recommendations</h3>
            <ul>
                ${analysis.recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
        </div>
    `;
}

// File upload preview
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('resume');
    const uploadText = document.querySelector('.upload-text');
    
    if (fileInput && uploadText) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                uploadText.textContent = this.files[0].name;
            }
        });
    }
});
