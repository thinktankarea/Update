import os
import numpy as np
from typing import List, Optional
from abc import ABC, abstractmethod
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer
import requests
import json


class BaseEmbeddingProvider(ABC):
    """Base class for embedding providers."""
    
    @abstractmethod
    def get_embeddings(self) -> Embeddings:
        """Get the embeddings instance."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available."""
        pass


class SentenceTransformerEmbeddings(Embeddings):
    """Sentence Transformers embeddings implementation."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model."""
        try:
            self._model = SentenceTransformer(self.model_name)
        except Exception as e:
            print(f"Error loading model {self.model_name}: {e}")
            # Fallback to a minimal model
            try:
                self._model = SentenceTransformer("all-MiniLM-L6-v2")
            except:
                self._model = None
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        if self._model is None:
            # Return dummy embeddings if model failed to load
            return [[0.0] * 384 for _ in texts]
        
        try:
            embeddings = self._model.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            print(f"Error embedding documents: {e}")
            return [[0.0] * 384 for _ in texts]
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query."""
        if self._model is None:
            return [0.0] * 384
        
        try:
            embedding = self._model.encode([text], convert_to_tensor=False)
            return embedding[0].tolist()
        except Exception as e:
            print(f"Error embedding query: {e}")
            return [0.0] * 384


class HuggingFaceAPIEmbeddings(Embeddings):
    """Hugging Face API embeddings implementation."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key or os.environ.get('HUGGINGFACE_API_KEY')
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_name}"
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents using HF API."""
        if not self.api_key:
            # Fallback to local embeddings
            local_embeddings = SentenceTransformerEmbeddings()
            return local_embeddings.embed_documents(texts)
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            all_embeddings = []
            for text in texts:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json={"inputs": text},
                    timeout=30
                )
                
                if response.status_code == 200:
                    embedding = response.json()
                    if isinstance(embedding, list) and len(embedding) > 0:
                        all_embeddings.append(embedding)
                    else:
                        all_embeddings.append([0.0] * 384)
                else:
                    all_embeddings.append([0.0] * 384)
            
            return all_embeddings
            
        except Exception as e:
            print(f"Error with HF API embeddings: {e}")
            # Fallback to local
            local_embeddings = SentenceTransformerEmbeddings()
            return local_embeddings.embed_documents(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query using HF API."""
        result = self.embed_documents([text])
        return result[0] if result else [0.0] * 384


class LocalEmbeddingProvider(BaseEmbeddingProvider):
    """Local sentence transformers provider."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
    
    def get_embeddings(self) -> Embeddings:
        return SentenceTransformerEmbeddings(model_name=self.model_name)
    
    def is_available(self) -> bool:
        """Check if sentence transformers is available."""
        try:
            import sentence_transformers
            return True
        except ImportError:
            return False


class HuggingFaceEmbeddingProvider(BaseEmbeddingProvider):
    """Hugging Face API embedding provider."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
    
    def get_embeddings(self) -> Embeddings:
        return HuggingFaceAPIEmbeddings(model_name=self.model_name, api_key=self.api_key)
    
    def is_available(self) -> bool:
        """Check if HF API is available."""
        return self.api_key is not None


class FallbackEmbeddings(Embeddings):
    """Simple fallback embeddings using basic text processing."""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Create simple hash-based embeddings."""
        embeddings = []
        for text in texts:
            # Create a simple hash-based embedding
            text_hash = hash(text.lower())
            # Convert to a vector of specified dimension
            embedding = [(text_hash + i) % 1000 / 1000.0 for i in range(self.dimension)]
            embeddings.append(embedding)
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """Create simple hash-based embedding for query."""
        result = self.embed_documents([text])
        return result[0]


class FallbackEmbeddingProvider(BaseEmbeddingProvider):
    """Fallback embedding provider that always works."""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
    
    def get_embeddings(self) -> Embeddings:
        return FallbackEmbeddings(dimension=self.dimension)
    
    def is_available(self) -> bool:
        return True


class EmbeddingFactory:
    """Factory for creating embedding providers."""
    
    @staticmethod
    def create_provider(provider_type: str, **kwargs) -> BaseEmbeddingProvider:
        """Create embedding provider based on type."""
        if provider_type.lower() == "local":
            return LocalEmbeddingProvider(**kwargs)
        elif provider_type.lower() == "huggingface":
            return HuggingFaceEmbeddingProvider(**kwargs)
        elif provider_type.lower() == "fallback":
            return FallbackEmbeddingProvider(**kwargs)
        else:
            return LocalEmbeddingProvider(**kwargs)
    
    @staticmethod
    def get_best_available_provider(**config) -> BaseEmbeddingProvider:
        """Get the best available embedding provider."""
        model_name = config.get('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
        api_key = config.get('HUGGINGFACE_API_KEY')
        
        # Try local first (best performance)
        local_provider = LocalEmbeddingProvider(model_name=model_name)
        if local_provider.is_available():
            return local_provider
        
        # Try Hugging Face API if key is available
        if api_key:
            hf_provider = HuggingFaceEmbeddingProvider(
                model_name=f"sentence-transformers/{model_name}",
                api_key=api_key
            )
            if hf_provider.is_available():
                return hf_provider
        
        # Fallback to simple embeddings
        return FallbackEmbeddingProvider()