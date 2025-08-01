import os
import PyPDF2
from typing import List, Dict, Any, Optional
from langchain.docstore.document import Document
import mimetypes
from werkzeug.utils import secure_filename


class FileProcessor:
    """Handles file upload and processing for various file types."""
    
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'py', 'js', 'java', 'cpp', 'c', 'html', 'css', 'md'}
    
    @staticmethod
    def is_allowed_file(filename: str) -> bool:
        """Check if file extension is allowed."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in FileProcessor.ALLOWED_EXTENSIONS
    
    @staticmethod
    def process_uploaded_file(file_path: str, filename: str) -> List[Document]:
        """Process uploaded file and return documents."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext == 'pdf':
            return FileProcessor._process_pdf(file_path, filename)
        else:
            return FileProcessor._process_text_file(file_path, filename)
    
    @staticmethod
    def _process_pdf(file_path: str, filename: str) -> List[Document]:
        """Process PDF file and extract text."""
        documents = []
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        if text.strip():  # Only add non-empty pages
                            doc = Document(
                                page_content=text,
                                metadata={
                                    "source": filename,
                                    "page": page_num + 1,
                                    "file_type": "pdf",
                                    "total_pages": len(pdf_reader.pages)
                                }
                            )
                            documents.append(doc)
                    except Exception as e:
                        print(f"Error processing page {page_num + 1}: {e}")
                        continue
                        
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
        
        return documents
    
    @staticmethod
    def _process_text_file(file_path: str, filename: str) -> List[Document]:
        """Process text-based files."""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            content = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        content = file.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                raise Exception("Could not decode file with any supported encoding")
            
            file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'txt'
            
            # Determine file type
            file_type = "code" if file_ext in ['py', 'js', 'java', 'cpp', 'c', 'html', 'css'] else "text"
            
            doc = Document(
                page_content=content,
                metadata={
                    "source": filename,
                    "file_type": file_type,
                    "language": file_ext,
                    "size": len(content)
                }
            )
            
            return [doc]
            
        except Exception as e:
            raise Exception(f"Error processing text file: {str(e)}")
    
    @staticmethod
    def save_uploaded_file(file, upload_folder: str) -> str:
        """Save uploaded file and return the file path."""
        if not file or file.filename == '':
            raise ValueError("No file selected")
        
        if not FileProcessor.is_allowed_file(file.filename):
            raise ValueError(f"File type not allowed. Allowed types: {', '.join(FileProcessor.ALLOWED_EXTENSIONS)}")
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Ensure upload folder exists
        os.makedirs(upload_folder, exist_ok=True)
        
        # Generate unique filename if file already exists
        base_name, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(upload_folder, filename)):
            filename = f"{base_name}_{counter}{ext}"
            counter += 1
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        return file_path
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """Get information about a file."""
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        stat = os.stat(file_path)
        filename = os.path.basename(file_path)
        
        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        
        return {
            "filename": filename,
            "size": stat.st_size,
            "size_human": FileProcessor._format_file_size(stat.st_size),
            "mime_type": mime_type,
            "extension": filename.rsplit('.', 1)[1].lower() if '.' in filename else '',
            "is_allowed": FileProcessor.is_allowed_file(filename)
        }
    
    @staticmethod
    def _format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024.0 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f}{size_names[i]}"
    
    @staticmethod
    def cleanup_file(file_path: str) -> bool:
        """Clean up uploaded file."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {e}")
            return False


class DocumentProcessor:
    """Process documents for semantic memory storage."""
    
    @staticmethod
    def prepare_documents_for_storage(documents: List[Document], source_info: Optional[Dict[str, Any]] = None) -> List[Document]:
        """Prepare documents for storage in semantic memory."""
        processed_docs = []
        
        for doc in documents:
            # Add additional metadata
            enhanced_metadata = doc.metadata.copy()
            
            if source_info:
                enhanced_metadata.update(source_info)
            
            # Add processing timestamp
            from datetime import datetime
            enhanced_metadata["processed_at"] = datetime.now().isoformat()
            
            # Create new document with enhanced metadata
            processed_doc = Document(
                page_content=doc.page_content,
                metadata=enhanced_metadata
            )
            processed_docs.append(processed_doc)
        
        return processed_docs
    
    @staticmethod
    def extract_code_snippets(document: Document) -> List[Document]:
        """Extract code snippets from documents."""
        if document.metadata.get("file_type") != "code":
            return [document]
        
        content = document.page_content
        language = document.metadata.get("language", "")
        
        # Simple code block extraction (can be enhanced)
        # For now, just return the whole document
        # In a more sophisticated version, you could parse functions, classes, etc.
        
        return [document]