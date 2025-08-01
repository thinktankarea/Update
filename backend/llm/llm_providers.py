import os
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
import requests
import json


class BaseLLMProvider(ABC):
    """Base class for LLM providers."""
    
    @abstractmethod
    def get_llm(self) -> LLM:
        """Get the LLM instance."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available."""
        pass


class HuggingFaceLLM(LLM):
    """Custom Hugging Face LLM implementation."""
    
    model_name: str = "microsoft/DialoGPT-medium"
    api_key: Optional[str] = None
    max_length: int = 512
    temperature: float = 0.7
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium", api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.model_name = model_name
        self.api_key = api_key or os.environ.get('HUGGINGFACE_API_KEY')
    
    @property
    def _llm_type(self) -> str:
        return "huggingface"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[list] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the Hugging Face model."""
        try:
            # Use Hugging Face Inference API
            if self.api_key:
                return self._call_api(prompt)
            else:
                return self._call_local(prompt)
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _call_api(self, prompt: str) -> str:
        """Call Hugging Face API."""
        url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": self.max_length,
                "temperature": self.temperature,
                "return_full_text": False
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "No response generated")
        return "No response generated"
    
    def _call_local(self, prompt: str) -> str:
        """Fallback to local processing or simple responses."""
        # This is a fallback for when no API key is available
        # In a real implementation, you might use transformers library here
        
        # Simple rule-based responses for common CS topics
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["hello", "hi", "help"]):
            return "Hello! I'm your CS lab instructor. I can help you with programming questions, explain code, run Python examples, and search for technical information. What would you like to learn today?"
        
        elif any(word in prompt_lower for word in ["python", "variable", "function"]):
            return """Here are some Python basics:

**Variables**: Store data using assignment
```python
name = "Alice"
age = 25
```

**Functions**: Reusable blocks of code
```python
def greet(name):
    return f"Hello, {name}!"
```

**Common data types**: int, str, list, dict
Would you like me to explain any specific concept in more detail?"""
        
        elif any(word in prompt_lower for word in ["javascript", "js", "web"]):
            return """JavaScript fundamentals:

**Variables**: 
```javascript
let name = "Alice";
const age = 25;
```

**Functions**:
```javascript
function greet(name) {
    return `Hello, ${name}!`;
}
```

**DOM manipulation**: document.getElementById(), addEventListener()
Need help with a specific JavaScript concept?"""
        
        elif any(word in prompt_lower for word in ["algorithm", "sort", "search"]):
            return """Common algorithms:

**Sorting**:
- Bubble Sort: O(n²) - Simple but inefficient
- Quick Sort: O(n log n) average - Divide and conquer
- Merge Sort: O(n log n) - Stable, predictable

**Searching**:
- Linear Search: O(n) - Check each element
- Binary Search: O(log n) - Requires sorted array

Would you like me to show you implementation examples?"""
        
        else:
            return f"""I understand you're asking about: {prompt[:100]}...

As your CS lab instructor, I can help with:
- Programming concepts and syntax
- Code explanation and debugging
- Algorithm explanations
- Running Python code examples
- Searching for technical resources

Please ask a more specific question, or try commands like:
- "Explain Python functions"
- "Show me a sorting algorithm"
- "Help with JavaScript arrays"
"""


class OllamaLLM(LLM):
    """Ollama local LLM implementation."""
    
    model_name: str = "llama2"
    base_url: str = "http://localhost:11434"
    
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(**kwargs)
        self.model_name = model_name
        self.base_url = base_url
    
    @property
    def _llm_type(self) -> str:
        return "ollama"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[list] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call Ollama API."""
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "No response generated")
            
        except requests.exceptions.ConnectionError:
            return "Ollama server is not running. Please start Ollama and try again."
        except Exception as e:
            return f"Error calling Ollama: {str(e)}"


class HuggingFaceProvider(BaseLLMProvider):
    """Hugging Face LLM provider."""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
    
    def get_llm(self) -> LLM:
        return HuggingFaceLLM(model_name=self.model_name, api_key=self.api_key)
    
    def is_available(self) -> bool:
        return True  # Always available as fallback


class OllamaProvider(BaseLLMProvider):
    """Ollama LLM provider."""
    
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
    
    def get_llm(self) -> LLM:
        return OllamaLLM(model_name=self.model_name, base_url=self.base_url)
    
    def is_available(self) -> bool:
        """Check if Ollama server is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False


class LLMFactory:
    """Factory for creating LLM providers."""
    
    @staticmethod
    def create_provider(provider_type: str, **kwargs) -> BaseLLMProvider:
        """Create LLM provider based on type."""
        if provider_type.lower() == "huggingface":
            return HuggingFaceProvider(**kwargs)
        elif provider_type.lower() == "ollama":
            return OllamaProvider(**kwargs)
        else:
            # Default to Hugging Face
            return HuggingFaceProvider(**kwargs)
    
    @staticmethod
    def get_best_available_provider(**config) -> BaseLLMProvider:
        """Get the best available provider based on configuration."""
        provider_type = config.get('LLM_PROVIDER', 'huggingface')
        
        # Try to create the preferred provider
        if provider_type.lower() == "ollama":
            ollama_provider = OllamaProvider(
                model_name=config.get('LLM_MODEL', 'llama2'),
                base_url=config.get('OLLAMA_BASE_URL', 'http://localhost:11434')
            )
            if ollama_provider.is_available():
                return ollama_provider
        
        # Fallback to Hugging Face
        return HuggingFaceProvider(
            model_name=config.get('LLM_MODEL', 'microsoft/DialoGPT-medium'),
            api_key=config.get('HUGGINGFACE_API_KEY')
        )