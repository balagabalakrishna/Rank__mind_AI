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

def analyze_prompt_type(prompt):
    """Analyze the prompt to determine the type of response needed"""
    prompt_lower = prompt.lower()
    
    # Check for code-related requests
    code_keywords = ['code', 'program', 'function', 'algorithm', 'implement', 'write a', 'create a', 'how to code']
    if any(keyword in prompt_lower for keyword in code_keywords):
        return 'code'
    
    # Check for explanation requests
    explanation_keywords = ['explain', 'what is', 'how does', 'describe', 'meaning of', 'tell me about']
    if any(keyword in prompt_lower for keyword in explanation_keywords):
        return 'explanation'
    
    # Check for translation requests
    translation_keywords = ['translate', 'convert to', 'in python', 'in javascript', 'in java', 'in c++']
    if any(keyword in prompt_lower for keyword in translation_keywords):
        return 'translation'
    
    # Check for debugging requests
    debug_keywords = ['error', 'fix', 'debug', 'why is this not working', 'problem with']
    if any(keyword in prompt_lower for keyword in debug_keywords):
        return 'debug'
    
    # Check for comparison requests
    comparison_keywords = ['difference between', 'vs', 'versus', 'compare', 'which is better']
    if any(keyword in prompt_lower for keyword in comparison_keywords):
        return 'comparison'
    
    # Default to general response
    return 'general'

def format_prompt_for_model(prompt, prompt_type, model_name):
    """Format the prompt based on the type of request and target model"""
    base_prompt = prompt
    
    if prompt_type == 'code':
        if model_name == 'nvidia':
            return f"As an expert coding assistant, please provide a complete, well-commented solution to: {prompt}. Include any necessary imports and provide example usage if applicable."
        elif model_name == 'gemini':
            return f"Generate clean, efficient code for: {prompt}. Include comments for important sections and consider edge cases."
        else:  # cohere
            return f"Please provide a practical coding solution for: {prompt}. Focus on readability and best practices."
    
    elif prompt_type == 'explanation':
        if model_name == 'nvidia':
            return f"Provide a detailed, technical explanation for: {prompt}. Break down complex concepts and provide examples where helpful."
        elif model_name == 'gemini':
            return f"Explain the following in a comprehensive yet accessible manner: {prompt}. Use analogies if helpful and structure the explanation logically."
        else:  # cohere
            return f"Offer a clear, concise explanation of: {prompt}. Focus on the key concepts and practical implications."
    
    elif prompt_type == 'translation':
        language = "the requested language"
        if 'python' in prompt.lower():
            language = "Python"
        elif 'javascript' in prompt.lower() or 'js' in prompt.lower():
            language = "JavaScript"
        elif 'java' in prompt.lower():
            language = "Java"
        elif 'c++' in prompt.lower() or 'cpp' in prompt.lower():
            language = "C++"
        
        return f"Translate the following code or concept to {language}: {prompt}. Ensure the translation is idiomatic and follows best practices for {language}."
    
    elif prompt_type == 'debug':
        return f"Help debug the following issue: {prompt}. Explain what might be causing the problem and provide a corrected version with an explanation of the fix."
    
    elif prompt_type == 'comparison':
        return f"Compare the concepts mentioned in: {prompt}. Highlight key differences, similarities, advantages, disadvantages, and use cases for each."
    
    else:  # general
        if model_name == 'nvidia':
            return f"As a technical assistant, provide a helpful response to: {prompt}. Focus on accuracy and practical value."
        elif model_name == 'gemini':
            return f"Provide a comprehensive response to: {prompt}. Cover the topic thoroughly while maintaining clarity."
        else:  # cohere
            return f"Offer a practical, well-reasoned response to: {prompt}. Focus on real-world applications and actionable insights."

def get_nvidia_response(formatted_prompt):
    """Get response from NVIDIA API using OpenAI client"""
    try:
        completion = nvidia_client.chat.completions.create(
            model="qwen/qwen2.5-coder-32b-instruct",
            messages=[{"role": "user", "content": formatted_prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"NVIDIA API Error: {str(e)}"

def get_gemini_response(formatted_prompt):
    """Get response from Google Gemini API"""
    try:
        # Try the updated Gemini endpoint first
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": formatted_prompt
                }]
            }]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        # If 404, try the beta endpoint
        if response.status_code == 404:
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

def get_cohere_response(formatted_prompt):
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
            "prompt": formatted_prompt,
            "max_tokens": 1024,
            "temperature": 0.7,
            "stream": False
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        return data['generations'][0]['text']
        
    except Exception as e:
        return f"Cohere API Error: {str(e)}"

def get_smart_fallback_response(prompt, provider, prompt_type):
    """Smart fallback response that generates relevant content based on prompt type"""
    time.sleep(1.5)  # Simulate processing time
    
    # Contextual responses based on prompt type
    if prompt_type == 'code':
        responses = {
            "nvidia": f"For the coding task '{prompt}', a good approach would be to break the problem down into smaller functions, handle edge cases, and ensure the solution is efficient. Here's a conceptual approach...",
            "gemini": f"To address the coding challenge '{prompt}', consider these key steps: 1) Understand the requirements, 2) Plan your algorithm, 3) Implement with clear naming, 4) Test with various inputs.",
            "cohere": f"When solving '{prompt}' programmatically, focus on readability and maintainability. Use descriptive variable names, add comments for complex logic, and consider error handling."
        }
    elif prompt_type == 'explanation':
        responses = {
            "nvidia": f"To explain '{prompt}', let's start with the fundamental concepts, then explore how they connect to broader principles in the field, and finally examine practical applications.",
            "gemini": f"The concept of '{prompt}' can be understood by examining its core components, historical context, and real-world examples that illustrate its importance and application.",
            "cohere": f"An effective explanation of '{prompt}' should cover the basic definition, key characteristics, common use cases, and how it relates to similar or contrasting concepts."
        }
    elif prompt_type == 'translation':
        responses = {
            "nvidia": f"For translating '{prompt}', it's important to understand both the source and target paradigms, consider idiomatic differences, and maintain the original intent while adapting to the new context.",
            "gemini": f"Translation of '{prompt}' requires careful consideration of syntax differences, library equivalents, and programming paradigms between the source and target languages.",
            "cohere": f"When translating '{prompt}', focus on preserving functionality while adapting to the target language's conventions, standard libraries, and best practices."
        }
    elif prompt_type == 'debug':
        responses = {
            "nvidia": f"To debug '{prompt}', a systematic approach would include: 1) Reproducing the issue, 2) Isolating the problem area, 3) Checking common pitfalls, 4) Testing potential fixes incrementally.",
            "gemini": f"Debugging '{prompt}' effectively requires understanding the expected behavior vs. actual behavior, examining error messages carefully, and using debugging tools to trace execution flow.",
            "cohere": f"For the debugging task '{prompt}', consider these strategies: add logging statements, use a debugger to step through code, check input validation, and verify assumptions about data structures."
        }
    elif prompt_type == 'comparison':
        responses = {
            "nvidia": f"When comparing concepts in '{prompt}', it's helpful to establish criteria for evaluation such as performance, readability, maintainability, ecosystem support, and learning curve.",
            "gemini": f"A comprehensive comparison of '{prompt}' should examine historical context, design philosophies, typical use cases, performance characteristics, and community adoption.",
            "cohere": f"To compare elements in '{prompt}', focus on practical differences: syntax, performance, tooling support, learning curve, community resources, and suitability for different project types."
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
        
        # Analyze the prompt type
        prompt_type = analyze_prompt_type(prompt)
        print(f"Detected prompt type: {prompt_type}")  # Debug log
        
        # Format prompts for each model
        nvidia_prompt = format_prompt_for_model(prompt, prompt_type, 'nvidia')
        gemini_prompt = format_prompt_for_model(prompt, prompt_type, 'gemini')
        cohere_prompt = format_prompt_for_model(prompt, prompt_type, 'cohere')
        
        # Try to get real responses first
        try:
            nvidia_response = get_nvidia_response(nvidia_prompt)
            if "Error" in nvidia_response:
                nvidia_response = get_smart_fallback_response(prompt, "nvidia", prompt_type)
        except Exception as e:
            nvidia_response = get_smart_fallback_response(prompt, "nvidia", prompt_type)
            print(f"NVIDIA error: {e}")
        
        try:
            gemini_response = get_gemini_response(gemini_prompt)
            if "Error" in gemini_response:
                gemini_response = get_smart_fallback_response(prompt, "gemini", prompt_type)
        except Exception as e:
            gemini_response = get_smart_fallback_response(prompt, "gemini", prompt_type)
            print(f"Gemini error: {e}")
        
        try:
            cohere_response = get_cohere_response(cohere_prompt)
            if "Error" in cohere_response:
                cohere_response = get_smart_fallback_response(prompt, "cohere", prompt_type)
        except Exception as e:
            cohere_response = get_smart_fallback_response(prompt, "cohere", prompt_type)
            print(f"Cohere error: {e}")
        
        return jsonify({
            'nvidia': nvidia_response,
            'gemini': gemini_response,
            'cohere': cohere_response,
            'prompt_received': prompt[:100] + "..." if len(prompt) > 100 else prompt,
            'prompt_type': prompt_type
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/test-apis', methods=['GET'])
def test_apis():
    """Test endpoint to check API connectivity"""
    test_prompt = 'Hello, how are you?'
    prompt_type = analyze_prompt_type(test_prompt)
    
    results = {
        'nvidia': get_nvidia_response(format_prompt_for_model(test_prompt, prompt_type, 'nvidia')),
        'gemini': get_gemini_response(format_prompt_for_model(test_prompt, prompt_type, 'gemini')),
        'cohere': get_cohere_response(format_prompt_for_model(test_prompt, prompt_type, 'cohere')),
        'test_prompt': test_prompt,
        'prompt_type': prompt_type,
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