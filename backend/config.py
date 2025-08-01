import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the Flask application."""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # API Keys (optional for some providers)
    HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
    TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')
    
    # LLM Configuration
    LLM_PROVIDER = os.environ.get('LLM_PROVIDER', 'huggingface')  # huggingface, ollama, or local
    LLM_MODEL = os.environ.get('LLM_MODEL', 'microsoft/DialoGPT-medium')
    EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'py', 'js', 'java', 'cpp', 'c'}
    
    # Memory configuration
    MEMORY_MAX_TOKEN_LIMIT = 2000
    FAISS_INDEX_PATH = 'faiss_index'
    
    @staticmethod
    def init_app(app):
        """Initialize the Flask app with configuration."""
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        if not os.path.exists(Config.FAISS_INDEX_PATH):
            os.makedirs(Config.FAISS_INDEX_PATH)