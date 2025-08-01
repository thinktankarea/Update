# AI-Powered CS Lab Instructor

A full-stack web application that serves as an adaptive AI-powered computer science lab instructor. This intelligent assistant helps students with programming tasks, explains code, executes Python examples, and maintains context across interactions using free AI models and services.

![CS Lab Instructor](https://img.shields.io/badge/AI-Powered-blue) ![Python](https://img.shields.io/badge/Python-3.9+-green) ![React](https://img.shields.io/badge/React-18+-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

### 🤖 **AI-Powered Instruction**
- Interactive chat interface with context-aware responses
- Patient, encouraging teaching style
- Step-by-step explanations of programming concepts

### 🐍 **Code Execution & Analysis**
- Safe Python code execution in isolated environment
- Multi-language code explanation (Python, JavaScript, Java, C++)
- Syntax analysis and best practices suggestions
- Live debugging assistance

### 🔍 **Research & Search**
- Web search integration for programming resources
- Documentation lookup and tutorial recommendations
- Fallback knowledge base for offline operation

### 📚 **Knowledge Management**
- Upload PDF lab manuals and documentation
- Semantic search through uploaded materials
- Persistent conversation memory
- Session-based learning context

### 🛠 **Developer Tools**
- File upload support (PDF, code files, text)
- Memory management (conversation + semantic)
- Session persistence
- Advanced debugging features

## Technology Stack

### Backend
- **Flask** - Web framework
- **LangChain** - AI agent orchestration
- **Hugging Face** - Free language models (fallback to rule-based)
- **FAISS** - Vector similarity search
- **Sentence Transformers** - Text embeddings
- **PyPDF2** - PDF processing

### Frontend
- **Next.js** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Radix UI** - Component library

### Free AI Services
- **Hugging Face Inference API** (optional, free tier)
- **Ollama** (local models, optional)
- **Tavily Search** (optional, free tier)
- **Fallback systems** for zero-dependency operation

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Git

### 1. Clone Repository
```bash
git clone <repository-url>
cd cs-lab-instructor
```

### 2. Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env file (optional - app works without API keys)
# Add your API keys if you have them:
# HUGGINGFACE_API_KEY=your_key_here
# TAVILY_API_KEY=your_key_here

# Start backend server
python app.py
```

### 3. Frontend Setup
```bash
# In a new terminal, navigate to project root
cd ..

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Set backend URL (if different from default)
echo "NEXT_PUBLIC_API_URL=http://localhost:5000" > .env.local

# Start frontend development server
npm run dev
```

### 4. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- API Health: http://localhost:5000/health

## Configuration

### Environment Variables

#### Backend (.env)
```bash
# LLM Configuration
LLM_PROVIDER=huggingface          # huggingface, ollama, or local
LLM_MODEL=microsoft/DialoGPT-medium
EMBEDDING_MODEL=all-MiniLM-L6-v2

# API Keys (Optional)
HUGGINGFACE_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here

# Ollama Configuration (if using)
OLLAMA_BASE_URL=http://localhost:11434

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## Usage Guide

### Basic Interaction
1. **Ask Questions**: Type programming questions in natural language
2. **Code Analysis**: Paste code snippets for explanation and analysis
3. **Execute Python**: Request code examples that will be run safely
4. **Upload Files**: Drag and drop PDFs or code files for analysis

### Example Queries
- "Explain how Python functions work"
- "Show me a bubble sort algorithm"
- "Help me debug this code: [paste code]"
- "What are the best practices for JavaScript variables?"
- "Analyze this uploaded lab manual"

### File Upload
Supported formats:
- **PDFs**: Lab manuals, textbooks, documentation
- **Code**: .py, .js, .java, .cpp, .c, .html, .css
- **Text**: .txt, .md files

### Advanced Features
- **Session Management**: Each browser session maintains conversation history
- **Memory Controls**: Clear conversation or knowledge base
- **Reasoning Steps**: View AI's thinking process (Advanced mode)
- **Quick Actions**: Pre-built common queries

## Deployment

### Local Development with Docker
```bash
cd backend
docker-compose up --build
```

### Production Deployment

#### Backend (Render/Railway/Heroku)
1. Connect your repository
2. Set environment variables
3. Deploy with `backend/` as root directory
4. Use `python app.py` as start command

#### Frontend (Vercel/Netlify)
1. Connect your repository
2. Set build command: `npm run build`
3. Set environment variable: `NEXT_PUBLIC_API_URL`
4. Deploy

#### Full Stack (Docker Compose)
```bash
# Production deployment
docker-compose -f backend/docker-compose.yml up -d
```

## API Reference

### Core Endpoints

#### POST /query
Send message to AI instructor
```json
{
  "message": "Explain Python functions",
  "session_id": "optional-session-id"
}
```

#### POST /upload
Upload files to knowledge base
```bash
curl -X POST -F "file=@document.pdf" \
     -F "session_id=your-session" \
     http://localhost:5000/upload
```

#### GET /health
Health check endpoint
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

### Memory Management
- `GET /memory/stats` - Get memory statistics
- `POST /memory/clear` - Clear conversation or semantic memory
- `GET /documents` - List uploaded documents
- `GET /sessions` - List active sessions

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   Next.js       │────▶│   Flask API     │
│   Frontend      │     │   Backend       │
└─────────────────┘     └─────────────────┘
                                │
                        ┌───────┴───────┐
                        │               │
                ┌───────▼──────┐ ┌──────▼──────┐
                │  LangChain   │ │   Memory    │
                │   Agent      │ │  Systems    │
                └───────┬──────┘ └──────┬──────┘
                        │               │
            ┌───────────┼───────────────┼──────────┐
            │           │               │          │
    ┌───────▼──┐ ┌──────▼──┐ ┌─────────▼──┐ ┌────▼────┐
    │ Python   │ │  Code   │ │ Hugging    │ │ FAISS   │
    │ REPL     │ │ Explain │ │ Face LLM   │ │ Vector  │
    │ Tool     │ │ Tool    │ │            │ │ Store   │
    └──────────┘ └─────────┘ └────────────┘ └─────────┘
```

## Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Guidelines
- Follow Python PEP 8 for backend code
- Use TypeScript for frontend development
- Add tests for new features
- Update documentation

## Troubleshooting

### Common Issues

#### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Verify dependencies
pip install -r backend/requirements.txt

# Check for port conflicts
lsof -i :5000
```

#### Frontend build errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 18+
```

#### CORS errors
- Ensure `NEXT_PUBLIC_API_URL` points to your backend
- Check that Flask-CORS is properly configured
- Verify backend is running on the correct port

#### Memory/Performance issues
- Restart the application to clear memory
- Use `/memory/clear` endpoint to reset conversation
- Check available disk space for uploads

### Logs and Debugging
- Backend logs: `backend/app.log`
- Browser console: Developer tools (F12)
- Health check: `curl http://localhost:5000/health`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **LangChain** for agent orchestration
- **Hugging Face** for free AI model access
- **Sentence Transformers** for embeddings
- **FAISS** for efficient similarity search
- **Next.js** and **Tailwind CSS** for beautiful UI

---

**Made with ❤️ for computer science education**

For issues and questions, please open a GitHub issue or contact the maintainers.