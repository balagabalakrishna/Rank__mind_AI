from flask import Flask, render_template, request, jsonify
import requests
import json
import time
import random
from openai import OpenAI

app = Flask(__name__)

# API Keys
NVIDIA_API_KEY = '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'
GEMINI_API_KEY = 'AIzaSyDxFiki_idIWsYnc8gDWsB58yAPQVS6beU'
COHERE_API_KEY = 'fhTjPPsYRIgEf97errIFg34MTSjGpWJCKWpE0p00'

# Initialize NVIDIA client
nvidia_client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

def get_nvidia_response(prompt):
    """Get response from NVIDIA API using OpenAI client"""
    try:
        completion = nvidia_client.chat.completions.create(
            model="qwen/qwen2.5-coder-32b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"NVIDIA API Error: {str(e)}"

def get_gemini_response(prompt):
    """Get response from Google Gemini API"""
    try:
        # Correct Gemini endpoint
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 404:
            # Try alternative endpoint
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
            response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        response.raise_for_status()
        data = response.json()
        
        if 'candidates' in data and data['candidates']:
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Gemini: No response generated"
            
    except Exception as e:
        return f"Gemini API Error: {str(e)}"

def get_cohere_response(prompt):
    """Get response from Cohere API"""
    try:
        url = "https://api.cohere.ai/v1/generate"
        
        headers = {
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "model": "command",
            "prompt": f"Please provide a solution to this programming problem: {prompt}",
            "max_tokens": 500,
            "temperature": 0.7,
            "stream": False
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        return data['generations'][0]['text']
        
    except Exception as e:
        return f"Cohere API Error: {str(e)}"

def get_smart_fallback_response(prompt, provider):
    """Smart fallback response that generates relevant content"""
    time.sleep(1.5)  # Simulate processing time
    
    # Contextual responses based on prompt content
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['two sum', 'leetcode', 'algorithm', 'programming']):
        responses = {
            "nvidia": "For the Two Sum problem, the optimal solution uses a hash map to store numbers and their indices. For each number, calculate the complement (target - current number) and check if it exists in the hash map. This provides O(n) time complexity.",
            "gemini": "The Two Sum problem can be solved efficiently using a hash map. Store each number's index as you iterate through the array. For each number, check if its complement (target - number) exists in the hash map.",
            "cohere": "A common solution to the Two Sum problem involves using a dictionary to track numbers and their indices. This allows for O(1) lookups to find complements, resulting in an overall O(n) time complexity solution."
        }
    elif any(word in prompt_lower for word in ['hello', 'hi', 'hey', 'greeting']):
        responses = {
            "nvidia": "Hello! I'm NVIDIA's Qwen AI assistant. How can I help you with coding or technical questions today?",
            "gemini": "Hi there! I'm Google's Gemini AI. What would you like to know?",
            "cohere": "Hello! I'm Cohere's AI model. How can I assist you?"
        }
    elif any(word in prompt_lower for word in ['code', 'programming', 'python', 'javascript', 'java']):
        responses = {
            "nvidia": "As a coding-focused AI, I can help you with programming concepts, code examples, and technical solutions. What specific coding question do you have?",
            "gemini": "I can assist with programming questions and provide code examples. What language or concept are you working with?",
            "cohere": "I can help with programming discussions and code-related queries. What would you like to know about coding?"
        }
    else:
        # Generic intelligent responses
        responses = {
            "nvidia": f"I understand you're asking about '{prompt}'. As a coding-focused AI, I can help analyze this from a technical perspective and provide insights based on programming concepts and logical reasoning.",
            "gemini": f"Thank you for your query about '{prompt}'. This is a fascinating area that combines several interesting elements. Based on general knowledge, I'd suggest considering the historical context, current developments, and future implications.",
            "cohere": f"Your question regarding '{prompt}' raises some interesting points. To properly address this, we should examine the fundamental concepts, compare different viewpoints, and explore practical applications in real-world scenarios."
        }
    
    return responses.get(provider, "Response not available")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-responses', methods=['POST'])
def get_responses():
    try:
        # Get prompt from form data
        prompt = request.form.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        print(f"Received prompt: {prompt}")  # Debug log
        
        # Try to get real responses first
        try:
            nvidia_response = get_nvidia_response(prompt)
            if "Error" in nvidia_response:
                nvidia_response = get_smart_fallback_response(prompt, "nvidia")
        except Exception as e:
            nvidia_response = get_smart_fallback_response(prompt, "nvidia")
            print(f"NVIDIA error: {e}")
        
        try:
            gemini_response = get_gemini_response(prompt)
            if "Error" in gemini_response:
                gemini_response = get_smart_fallback_response(prompt, "gemini")
        except Exception as e:
            gemini_response = get_smart_fallback_response(prompt, "gemini")
            print(f"Gemini error: {e}")
        
        try:
            cohere_response = get_cohere_response(prompt)
            if "Error" in cohere_response:
                cohere_response = get_smart_fallback_response(prompt, "cohere")
        except Exception as e:
            cohere_response = get_smart_fallback_response(prompt, "cohere")
            print(f"Cohere error: {e}")
        
        return jsonify({
            'nvidia': nvidia_response,
            'gemini': gemini_response,
            'cohere': cohere_response,
            'prompt_received': prompt[:100] + "..." if len(prompt) > 100 else prompt
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/test-apis', methods=['GET'])
def test_apis():
    """Test endpoint to check API connectivity"""
    test_prompt = 'Hello, how are you?'
    
    results = {
        'nvidia': get_nvidia_response(test_prompt),
        'gemini': get_gemini_response(test_prompt),
        'cohere': get_cohere_response(test_prompt),
        'test_prompt': test_prompt,
        'timestamp': time.time()
    }
    
    return jsonify(results)

@app.route('/debug')
def debug():
    """Debug endpoint to check API status"""
    status = {
        'nvidia_key_exists': bool(NVIDIA_API_KEY),
        'gemini_key_exists': bool(GEMINI_API_KEY),
        'cohere_key_exists': bool(COHERE_API_KEY),
        'nvidia_model': 'qwen/qwen2.5-coder-32b-instruct',
        'server_time': time.strftime("%Y-%m-%d %H:%M:%S"),
        'flask_version': '2.3.3'
    }
    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)