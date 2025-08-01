import os
import pickle
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
import hashlib
from datetime import datetime


class SemanticMemory:
    """FAISS-based semantic memory for storing and retrieving documents."""
    
    def __init__(self, index_path: str = "faiss_index", embeddings_model: str = "text-embedding-ada-002"):
        self.index_path = index_path
        self.embeddings = OpenAIEmbeddings(model=embeddings_model)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.vectorstore = None
        self.metadata_file = os.path.join(index_path, "metadata.pkl")
        self.document_metadata = {}
        
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self) -> None:
        """Initialize or load existing FAISS vectorstore."""
        try:
            if os.path.exists(self.index_path) and os.path.exists(os.path.join(self.index_path, "index.faiss")):
                # Load existing vectorstore
                self.vectorstore = FAISS.load_local(self.index_path, self.embeddings)
                self._load_metadata()
                print(f"Loaded existing FAISS index from {self.index_path}")
            else:
                # Create new vectorstore with dummy document
                dummy_doc = Document(page_content="Initialize", metadata={"source": "system"})
                self.vectorstore = FAISS.from_documents([dummy_doc], self.embeddings)
                os.makedirs(self.index_path, exist_ok=True)
                self.save_index()
                print(f"Created new FAISS index at {self.index_path}")
        except Exception as e:
            print(f"Error initializing vectorstore: {e}")
            # Fallback to new vectorstore
            dummy_doc = Document(page_content="Initialize", metadata={"source": "system"})
            self.vectorstore = FAISS.from_documents([dummy_doc], self.embeddings)
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to the semantic memory."""
        try:
            # Split documents into chunks
            doc_chunks = self.text_splitter.split_documents(documents)
            
            # Generate document IDs
            doc_ids = []
            for chunk in doc_chunks:
                content_hash = hashlib.md5(chunk.page_content.encode()).hexdigest()
                doc_id = f"doc_{content_hash[:8]}"
                doc_ids.append(doc_id)
                
                # Add metadata
                chunk.metadata.update({
                    "doc_id": doc_id,
                    "added_at": datetime.now().isoformat(),
                    "chunk_size": len(chunk.page_content)
                })
            
            # Add to vectorstore
            if self.vectorstore is None:
                self.vectorstore = FAISS.from_documents(doc_chunks, self.embeddings)
            else:
                self.vectorstore.add_documents(doc_chunks)
            
            # Update metadata
            for doc_id, chunk in zip(doc_ids, doc_chunks):
                self.document_metadata[doc_id] = {
                    "content": chunk.page_content,
                    "metadata": chunk.metadata,
                    "added_at": datetime.now().isoformat()
                }
            
            self.save_index()
            return doc_ids
            
        except Exception as e:
            print(f"Error adding documents: {e}")
            return []
    
    def add_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add a single text to semantic memory."""
        if metadata is None:
            metadata = {}
        
        doc = Document(page_content=text, metadata=metadata)
        doc_ids = self.add_documents([doc])
        return doc_ids[0] if doc_ids else ""
    
    def search_similar(self, query: str, k: int = 5, score_threshold: float = 0.7) -> List[Tuple[Document, float]]:
        """Search for similar documents."""
        try:
            if self.vectorstore is None:
                return []
            
            # Perform similarity search with scores
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            
            # Filter by score threshold
            filtered_results = [
                (doc, score) for doc, score in results 
                if score >= score_threshold and doc.page_content != "Initialize"
            ]
            
            return filtered_results
            
        except Exception as e:
            print(f"Error searching similar documents: {e}")
            return []
    
    def search_by_metadata(self, metadata_filter: Dict[str, Any]) -> List[Document]:
        """Search documents by metadata criteria."""
        matching_docs = []
        
        for doc_id, doc_data in self.document_metadata.items():
            doc_metadata = doc_data.get("metadata", {})
            
            # Check if all filter criteria match
            match = True
            for key, value in metadata_filter.items():
                if key not in doc_metadata or doc_metadata[key] != value:
                    match = False
                    break
            
            if match:
                content = doc_data.get("content", "")
                doc = Document(page_content=content, metadata=doc_metadata)
                matching_docs.append(doc)
        
        return matching_docs
    
    def get_relevant_context(self, query: str, max_chunks: int = 3) -> str:
        """Get relevant context for a query."""
        similar_docs = self.search_similar(query, k=max_chunks)
        
        if not similar_docs:
            return "No relevant context found in semantic memory."
        
        context_parts = []
        for i, (doc, score) in enumerate(similar_docs, 1):
            source = doc.metadata.get("source", "Unknown")
            context_parts.append(f"**Context {i}** (from {source}):\n{doc.page_content}")
        
        return "\n\n".join(context_parts)
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document by its ID."""
        try:
            if doc_id in self.document_metadata:
                del self.document_metadata[doc_id]
                self.save_index()
                return True
            return False
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def clear_memory(self) -> None:
        """Clear all semantic memory."""
        try:
            # Create new empty vectorstore
            dummy_doc = Document(page_content="Initialize", metadata={"source": "system"})
            self.vectorstore = FAISS.from_documents([dummy_doc], self.embeddings)
            self.document_metadata.clear()
            self.save_index()
            print("Semantic memory cleared")
        except Exception as e:
            print(f"Error clearing memory: {e}")
    
    def save_index(self) -> None:
        """Save the FAISS index and metadata."""
        try:
            if self.vectorstore is not None:
                self.vectorstore.save_local(self.index_path)
            
            # Save metadata
            with open(self.metadata_file, 'wb') as f:
                pickle.dump(self.document_metadata, f)
                
        except Exception as e:
            print(f"Error saving index: {e}")
    
    def _load_metadata(self) -> None:
        """Load document metadata."""
        try:
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'rb') as f:
                    self.document_metadata = pickle.load(f)
        except Exception as e:
            print(f"Error loading metadata: {e}")
            self.document_metadata = {}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the semantic memory."""
        try:
            if self.vectorstore is None:
                return {"total_documents": 0, "total_chunks": 0}
            
            total_docs = len(self.document_metadata)
            total_chunks = len(self.vectorstore.docstore._dict) - 1  # Exclude dummy doc
            
            return {
                "total_documents": total_docs,
                "total_chunks": max(0, total_chunks),
                "index_path": self.index_path,
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {"error": str(e)}
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents in memory."""
        docs_list = []
        for doc_id, doc_data in self.document_metadata.items():
            docs_list.append({
                "doc_id": doc_id,
                "metadata": doc_data.get("metadata", {}),
                "content_preview": doc_data.get("content", "")[:100] + "...",
                "added_at": doc_data.get("added_at", "Unknown")
            })
        return docs_list