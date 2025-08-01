import os
from typing import Optional, Dict, Any
from langchain.tools import BaseTool
from pydantic import Field
import requests
import json


class TavilySearchTool(BaseTool):
    """Tool for performing web searches using Tavily API."""
    
    name: str = "tavily_search"
    description: str = """
    Search the web for current information on programming topics, documentation, tutorials, and technical resources.
    Useful for finding up-to-date information, code examples, and solving programming problems.
    Input should be a search query string.
    """
    
    api_key: Optional[str] = Field(default=None)
    
    def __init__(self, **data):
        super().__init__(**data)
        if not self.api_key:
            self.api_key = os.environ.get('TAVILY_API_KEY')
    
    def _run(self, query: str) -> str:
        """Perform a web search using Tavily."""
        if not self.api_key:
            return "Error: Tavily API key not configured. Please set TAVILY_API_KEY environment variable."
        
        try:
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": self.api_key,
                "query": query,
                "search_depth": "basic",
                "include_answer": True,
                "include_images": False,
                "include_raw_content": False,
                "max_results": 5
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Format the response
            if 'results' in data:
                formatted_results = []
                
                # Include the answer if available
                if data.get('answer'):
                    formatted_results.append(f"**Answer:** {data['answer']}\n")
                
                # Add search results
                formatted_results.append("**Search Results:**")
                for i, result in enumerate(data['results'][:3], 1):
                    title = result.get('title', 'No title')
                    content = result.get('content', 'No content')
                    url = result.get('url', 'No URL')
                    
                    formatted_results.append(f"\n{i}. **{title}**")
                    formatted_results.append(f"   {content[:200]}...")
                    formatted_results.append(f"   Source: {url}")
                
                return "\n".join(formatted_results)
            else:
                return "No search results found."
                
        except requests.exceptions.RequestException as e:
            return f"Search request failed: {str(e)}"
        except Exception as e:
            return f"Search error: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of _run."""
        return self._run(query)


class FallbackSearchTool(BaseTool):
    """Fallback search tool that doesn't require API keys."""
    
    name: str = "fallback_search"
    description: str = """
    Provides general programming knowledge and common solutions for coding problems.
    Use when external search is not available.
    """
    
    def _run(self, query: str) -> str:
        """Provide fallback search responses."""
        knowledge_base = {
            "python": {
                "keywords": ["python", "py", "django", "flask", "pandas", "numpy"],
                "response": """
                Python is a high-level programming language known for its simplicity and readability.
                
                Common Python concepts:
                - Variables and data types (int, str, list, dict)
                - Control structures (if/else, for/while loops)
                - Functions and classes
                - Modules and packages
                - Exception handling with try/except
                
                Popular libraries:
                - NumPy: Numerical computing
                - Pandas: Data manipulation
                - Flask/Django: Web development
                - Requests: HTTP requests
                """
            },
            "javascript": {
                "keywords": ["javascript", "js", "node", "react", "vue", "angular"],
                "response": """
                JavaScript is a versatile programming language for web development.
                
                Key concepts:
                - Variables (var, let, const)
                - Functions and arrow functions
                - Objects and arrays
                - DOM manipulation
                - Async programming (promises, async/await)
                - ES6+ features
                
                Frameworks and libraries:
                - React: UI library
                - Vue.js: Progressive framework
                - Node.js: Server-side JavaScript
                - Express.js: Web framework
                """
            },
            "algorithms": {
                "keywords": ["algorithm", "sorting", "searching", "complexity", "big o"],
                "response": """
                Common algorithms and data structures:
                
                Sorting algorithms:
                - Bubble sort: O(n²)
                - Quick sort: O(n log n) average
                - Merge sort: O(n log n)
                
                Search algorithms:
                - Linear search: O(n)
                - Binary search: O(log n)
                
                Data structures:
                - Arrays, Linked Lists
                - Stacks, Queues
                - Trees, Graphs
                - Hash Tables
                """
            }
        }
        
        query_lower = query.lower()
        
        for topic, info in knowledge_base.items():
            if any(keyword in query_lower for keyword in info["keywords"]):
                return f"**{topic.title()} Information:**\n{info['response']}"
        
        return f"""
        I couldn't find specific information about "{query}". Here are some general programming resources:
        
        **Common Programming Concepts:**
        - Variables and data types
        - Control structures (loops, conditionals)
        - Functions and methods
        - Object-oriented programming
        - Error handling
        - Testing and debugging
        
        **Best Practices:**
        - Write clean, readable code
        - Use meaningful variable names
        - Comment your code
        - Follow language-specific style guides
        - Test your code regularly
        
        Please provide more specific details about what you're looking for.
        """
    
    async def _arun(self, query: str) -> str:
        """Async version of _run."""
        return self._run(query)