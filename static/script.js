document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prompt-form');
    const responsesContainer = document.getElementById('responses-container');
    const loading = document.getElementById('loading');
    const submitBtn = document.getElementById('submit-btn');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const prompt = document.getElementById('prompt').value.trim();
        
        if (!prompt) {
            alert('Please enter a prompt');
            return;
        }
        
        // Show loading, hide responses
        loading.style.display = 'flex';
        responsesContainer.style.display = 'none';
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';
        
        // Send request to server
        fetch('/get-responses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'prompt': prompt
            })
        })
        .then(response => response.json())
        .then(data => {
            // Display responses
            document.getElementById('nvidia-response').textContent = data.nvidia;
            document.getElementById('gemini-response').textContent = data.gemini;
            document.getElementById('cohere-response').textContent = data.cohere;
            
            // Show responses, hide loading
            responsesContainer.style.display = 'flex';
            loading.style.display = 'none';
            submitBtn.disabled = false;
            submitBtn.textContent = 'Get Responses';
            
            // Scroll to results
            responsesContainer.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching responses');
            loading.style.display = 'none';
            submitBtn.disabled = false;
            submitBtn.textContent = 'Get Responses';
        });
    });
});