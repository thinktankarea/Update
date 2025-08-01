import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the Flask application."""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # API Keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')
    
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