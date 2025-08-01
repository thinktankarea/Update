# CS Lab Instructor - Backend

Flask-based backend API for the AI-powered CS lab instructor application.

## Architecture

The backend is built with a modular architecture:

```
backend/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── agent/                # AI agent implementation
│   └── cs_instructor_agent.py
├── llm/                  # LLM providers and embeddings
│   ├── llm_providers.py
│   └── embeddings.py
├── memory/               # Memory management
│   ├── conversation_memory.py
│   └── semantic_memory.py
├── tools/                # LangChain tools
│   ├── python_repl_tool.py
│   ├── search_tool.py
│   └── explain_code_tool.py
└── utils/                # Utilities
    └── file_processor.py
```

## Features

### AI Agent Capabilities
- **Context-aware conversations** using ConversationBufferMemory
- **Tool integration** for code execution, web search, and code analysis
- **Semantic memory** for document storage and retrieval
- **Session management** for multiple concurrent users

### Free AI Integration
- **Hugging Face Inference API** (optional, free tier)
- **Local sentence transformers** for embeddings
- **Ollama support** for local LLM hosting
- **Fallback systems** for operation without external APIs

### Safety Features
- **Sandboxed Python execution** with restricted imports
- **File upload validation** and secure processing
- **Memory limits** and cleanup mechanisms
- **Error handling** and logging throughout

## API Endpoints

### Core Functionality
- `POST /query` - Send messages to AI instructor
- `POST /upload` - Upload files to knowledge base
- `GET /health` - Health check endpoint

### Memory Management
- `GET /memory/stats` - Get memory statistics
- `POST /memory/clear` - Clear conversation or semantic memory
- `GET /documents` - List uploaded documents
- `GET /sessions` - List active sessions
- `GET /export/conversation` - Export conversation history

## Configuration

### Environment Variables
```bash
# LLM Configuration
LLM_PROVIDER=huggingface          # huggingface, ollama, or local
LLM_MODEL=microsoft/DialoGPT-medium
EMBEDDING_MODEL=all-MiniLM-L6-v2

# API Keys (Optional)
HUGGINGFACE_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### LLM Providers

#### Hugging Face (Recommended)
- Uses free Hugging Face Inference API
- Falls back to rule-based responses if no API key
- Supports various models including DialoGPT

#### Ollama (Local)
- Requires local Ollama installation
- Supports models like Llama 2, Code Llama
- Best for privacy and performance

#### Fallback (Always Available)
- Rule-based responses for common CS topics
- Works without any external dependencies
- Provides basic educational content

## Development

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start development server
python app.py
```

### Testing
```bash
# Test health endpoint
curl http://localhost:5000/health

# Test query endpoint
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'

# Test file upload
curl -X POST http://localhost:5000/upload \
  -F "file=@test.pdf"
```

### Docker
```bash
# Build and run with Docker
docker build -t cs-instructor-backend .
docker run -p 5000:5000 cs-instructor-backend

# Or use docker-compose
docker-compose up --build
```

## Deployment

### Render/Railway/Heroku
1. Set environment variables in platform dashboard
2. Use `python app.py` as start command
3. Ensure port is set via `PORT` environment variable

### Manual Server
```bash
# Install dependencies
pip install -r requirements.txt

# Set production environment
export FLASK_ENV=production
export FLASK_DEBUG=False

# Run with Gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Security Considerations

### Code Execution Safety
- Python REPL uses restricted builtins
- Blocked imports for dangerous modules
- AST parsing for code analysis
- Execution timeouts and memory limits

### File Upload Security
- Filename sanitization
- File type validation
- Size limits (16MB default)
- Temporary file cleanup

### API Security
- CORS configuration
- Input validation
- Error message sanitization
- Session isolation

## Monitoring and Logs

### Logging
- Application logs: `app.log`
- Structured logging with timestamps
- Error tracking with stack traces
- Performance metrics

### Health Checks
- `/health` endpoint for uptime monitoring
- Memory usage statistics
- Session count tracking

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python version (3.9+ required)
python --version
```

#### Memory Issues
```bash
# Clear FAISS index
rm -rf faiss_index/

# Clear sessions
rm -rf sessions/

# Restart application
```

#### Model Loading Errors
```bash
# For sentence-transformers issues
pip install sentence-transformers --upgrade

# For FAISS issues on M1 Macs
pip install faiss-cpu --no-cache-dir
```

## Contributing

### Code Structure
- Follow PEP 8 style guidelines
- Use type hints where possible
- Add docstrings to all classes and methods
- Include unit tests for new features

### Adding New Tools
1. Create tool class in `tools/` directory
2. Inherit from LangChain `BaseTool`
3. Implement `_run` and `_arun` methods
4. Add to agent's tool list in `cs_instructor_agent.py`

### Adding New LLM Providers
1. Create provider class in `llm/llm_providers.py`
2. Implement `BaseLLMProvider` interface
3. Add to `LLMFactory.create_provider` method
4. Update configuration documentation

## License

MIT License - see LICENSE file for details.