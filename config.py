import os

class Config:
    # API Keys - Replace with your actual keys or set as environment variables
    NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', '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')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDxFiki_idIWsYnc8gDWsB58yAPQVS6beU')
    COHERE_API_KEY = os.getenv('COHERE_API_KEY', 'fhTjPPsYRIgEf97errIFg34MTSjGpWJCKWpE0p00')
    
    # Add any other configuration settings here
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')