import os
import logging
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import traceback
import uuid
from datetime import datetime

from config import Config
from agent import CSInstructorAgent
from utils import FileProcessor, DocumentProcessor


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize configuration
    Config.init_app(app)
    
    # Enable CORS for all domains on all routes
    CORS(app, origins=["http://localhost:3000", "http://localhost:5000", "*"])
    
    # Global agent storage (in production, use Redis or database)
    agents = {}
    
    def get_or_create_agent(session_id: str = None) -> CSInstructorAgent:
        """Get existing agent or create new one."""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        if session_id not in agents:
            config_dict = {
                'HUGGINGFACE_API_KEY': app.config.get('HUGGINGFACE_API_KEY'),
                'TAVILY_API_KEY': app.config.get('TAVILY_API_KEY'),
                'LLM_PROVIDER': app.config.get('LLM_PROVIDER'),
                'LLM_MODEL': app.config.get('LLM_MODEL'),
                'EMBEDDING_MODEL': app.config.get('EMBEDDING_MODEL'),
                'OLLAMA_BASE_URL': app.config.get('OLLAMA_BASE_URL'),
                'MEMORY_MAX_TOKEN_LIMIT': app.config.get('MEMORY_MAX_TOKEN_LIMIT'),
                'FAISS_INDEX_PATH': app.config.get('FAISS_INDEX_PATH')
            }
            agents[session_id] = CSInstructorAgent(config_dict, session_id)
            logger.info(f"Created new agent for session: {session_id}")
        
        return agents[session_id]
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
    
    @app.route('/query', methods=['POST'])
    def query():
        """Main query endpoint for the CS instructor."""
        try:
            data = request.get_json()
            
            if not data or 'message' not in data:
                return jsonify({
                    'error': 'Missing message in request body',
                    'success': False
                }), 400
            
            user_message = data['message']
            session_id = data.get('session_id')
            
            # Get or create agent
            agent = get_or_create_agent(session_id)
            
            # Process the query
            response = agent.query(user_message)
            
            logger.info(f"Query processed for session {agent.session_id}: {user_message[:50]}...")
            
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            logger.error(traceback.format_exc())
            
            return jsonify({
                'error': f'Internal server error: {str(e)}',
                'success': False,
                'response': 'I apologize, but I encountered an error. Please try again.'
            }), 500
    
    @app.route('/upload', methods=['POST'])
    def upload_file():
        """Upload and process files for the knowledge base."""
        try:
            if 'file' not in request.files:
                return jsonify({
                    'error': 'No file provided',
                    'success': False
                }), 400
            
            file = request.files['file']
            session_id = request.form.get('session_id')
            
            if file.filename == '':
                return jsonify({
                    'error': 'No file selected',
                    'success': False
                }), 400
            
            # Get or create agent
            agent = get_or_create_agent(session_id)
            
            # Save uploaded file
            file_path = FileProcessor.save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
            
            try:
                # Process the file
                documents = FileProcessor.process_uploaded_file(file_path, file.filename)
                
                # Add to semantic memory
                source_info = {
                    'upload_session': agent.session_id,
                    'original_filename': file.filename,
                    'upload_timestamp': datetime.now().isoformat()
                }
                
                result = agent.add_documents_to_memory(documents, source_info)
                
                # Get file info
                file_info = FileProcessor.get_file_info(file_path)
                
                # Clean up uploaded file
                FileProcessor.cleanup_file(file_path)
                
                logger.info(f"File uploaded and processed: {file.filename} for session {agent.session_id}")
                
                return jsonify({
                    'success': True,
                    'message': result['message'],
                    'file_info': file_info,
                    'documents_added': result['count'],
                    'session_id': agent.session_id
                })
                
            except Exception as e:
                # Clean up file on error
                FileProcessor.cleanup_file(file_path)
                raise e
                
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            logger.error(traceback.format_exc())
            
            return jsonify({
                'error': f'File upload failed: {str(e)}',
                'success': False
            }), 500
    
    @app.route('/memory/stats', methods=['GET'])
    def memory_stats():
        """Get memory statistics."""
        try:
            session_id = request.args.get('session_id')
            
            if not session_id or session_id not in agents:
                return jsonify({
                    'error': 'Invalid or missing session_id',
                    'success': False
                }), 400
            
            agent = agents[session_id]
            stats = agent.get_memory_stats()
            
            return jsonify({
                'success': True,
                'stats': stats
            })
            
        except Exception as e:
            logger.error(f"Error getting memory stats: {str(e)}")
            
            return jsonify({
                'error': f'Failed to get memory stats: {str(e)}',
                'success': False
            }), 500
    
    @app.route('/memory/clear', methods=['POST'])
    def clear_memory():
        """Clear conversation or semantic memory."""
        try:
            data = request.get_json()
            session_id = data.get('session_id')
            memory_type = data.get('type', 'conversation')  # 'conversation' or 'semantic'
            
            if not session_id or session_id not in agents:
                return jsonify({
                    'error': 'Invalid or missing session_id',
                    'success': False
                }), 400
            
            agent = agents[session_id]
            
            if memory_type == 'conversation':
                result = agent.clear_conversation_memory()
            elif memory_type == 'semantic':
                result = agent.clear_semantic_memory()
            else:
                return jsonify({
                    'error': 'Invalid memory type. Use "conversation" or "semantic"',
                    'success': False
                }), 400
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Error clearing memory: {str(e)}")
            
            return jsonify({
                'error': f'Failed to clear memory: {str(e)}',
                'success': False
            }), 500
    
    @app.route('/documents', methods=['GET'])
    def list_documents():
        """List documents in semantic memory."""
        try:
            session_id = request.args.get('session_id')
            
            if not session_id or session_id not in agents:
                return jsonify({
                    'error': 'Invalid or missing session_id',
                    'success': False
                }), 400
            
            agent = agents[session_id]
            documents = agent.list_documents()
            
            return jsonify({
                'success': True,
                'documents': documents,
                'count': len(documents)
            })
            
        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}")
            
            return jsonify({
                'error': f'Failed to list documents: {str(e)}',
                'success': False
            }), 500
    
    @app.route('/export/conversation', methods=['GET'])
    def export_conversation():
        """Export conversation history."""
        try:
            session_id = request.args.get('session_id')
            
            if not session_id or session_id not in agents:
                return jsonify({
                    'error': 'Invalid or missing session_id',
                    'success': False
                }), 400
            
            agent = agents[session_id]
            conversation = agent.export_conversation()
            
            return jsonify({
                'success': True,
                'conversation': conversation
            })
            
        except Exception as e:
            logger.error(f"Error exporting conversation: {str(e)}")
            
            return jsonify({
                'error': f'Failed to export conversation: {str(e)}',
                'success': False
            }), 500
    
    @app.route('/sessions', methods=['GET'])
    def list_sessions():
        """List active sessions."""
        try:
            session_info = []
            for session_id, agent in agents.items():
                stats = agent.get_memory_stats()
                session_info.append({
                    'session_id': session_id,
                    'conversation_summary': stats['conversation'],
                    'semantic_memory_stats': stats['semantic_memory']
                })
            
            return jsonify({
                'success': True,
                'sessions': session_info,
                'count': len(session_info)
            })
            
        except Exception as e:
            logger.error(f"Error listing sessions: {str(e)}")
            
            return jsonify({
                'error': f'Failed to list sessions: {str(e)}',
                'success': False
            }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({
            'error': 'Endpoint not found',
            'success': False
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            'error': 'Internal server error',
            'success': False
        }), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Check if running in debug mode
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"Starting CS Instructor API server on port {port}")
    logger.info(f"Debug mode: {debug_mode}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )