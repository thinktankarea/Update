import os
from typing import Dict, Any, List, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.schema import BaseMessage

from ..tools import PythonREPLTool, SafePythonREPLTool, TavilySearchTool, FallbackSearchTool, ExplainCodeTool
from ..memory import ConversationMemoryManager, SemanticMemory
from ..llm import LLMFactory


class CSInstructorAgent:
    """AI-powered CS lab instructor agent."""
    
    def __init__(self, config: Dict[str, Any], session_id: str = "default"):
        self.config = config
        self.session_id = session_id
        
        # Initialize memory
        self.conversation_memory = ConversationMemoryManager(
            max_token_limit=config.get('MEMORY_MAX_TOKEN_LIMIT', 2000),
            session_id=session_id
        )
        
        self.semantic_memory = SemanticMemory(
            index_path=config.get('FAISS_INDEX_PATH', 'faiss_index'),
            config=config
        )
        
        # Initialize LLM
        llm_provider = LLMFactory.get_best_available_provider(**config)
        self.llm = llm_provider.get_llm()
        
        # Initialize tools
        self.tools = self._initialize_tools()
        
        # Create agent
        self.agent_executor = self._create_agent()
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize all available tools."""
        tools = []
        
        # Code execution tool
        python_tool = SafePythonREPLTool()
        tools.append(Tool(
            name="execute_python",
            func=python_tool._run,
            description="Execute Python code safely. Use this to demonstrate code examples, run calculations, or help debug student code."
        ))
        
        # Code explanation tool
        explain_tool = ExplainCodeTool()
        tools.append(Tool(
            name="explain_code",
            func=explain_tool._run,
            description="Analyze and explain code snippets. Use this to help students understand code structure, syntax, and best practices."
        ))
        
        # Search tool (try Tavily first, fallback to local)
        try:
            if self.config.get('TAVILY_API_KEY'):
                search_tool = TavilySearchTool(api_key=self.config.get('TAVILY_API_KEY'))
            else:
                search_tool = FallbackSearchTool()
        except:
            search_tool = FallbackSearchTool()
        
        tools.append(Tool(
            name="search_information",
            func=search_tool._run,
            description="Search for programming information, documentation, tutorials, and solutions to coding problems."
        ))
        
        # Semantic memory search tool
        tools.append(Tool(
            name="search_knowledge_base",
            func=self._search_semantic_memory,
            description="Search the knowledge base for relevant information from uploaded documents, lab manuals, and previous conversations."
        ))
        
        return tools
    
    def _search_semantic_memory(self, query: str) -> str:
        """Search semantic memory for relevant context."""
        try:
            context = self.semantic_memory.get_relevant_context(query, max_chunks=3)
            return context
        except Exception as e:
            return f"Error searching knowledge base: {str(e)}"
    
    def _create_agent(self) -> AgentExecutor:
        """Create the ReAct agent."""
        prompt_template = """You are an AI-powered CS lab instructor helping students learn programming. 
You are knowledgeable, patient, and encouraging. Your goal is to help students understand concepts, 
debug code, and develop problem-solving skills.

You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Guidelines for being a good CS instructor:
1. Always explain concepts clearly and step by step
2. Provide examples when explaining programming concepts
3. Encourage best practices and point out common mistakes
4. When helping with code, explain the logic and reasoning
5. Use the code execution tool to demonstrate examples
6. Search for information when you need current or specific details
7. Break down complex problems into smaller, manageable parts
8. Be patient and supportive, especially with beginners

Previous conversation context:
{chat_history}

Question: {input}
{agent_scratchpad}"""

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["input", "chat_history", "agent_scratchpad"],
            partial_variables={
                "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools]),
                "tool_names": ", ".join([tool.name for tool in self.tools])
            }
        )
        
        # Create ReAct agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
    
    def query(self, user_input: str) -> Dict[str, Any]:
        """Process user query and return response."""
        try:
            # Get conversation history
            chat_history = self.conversation_memory.get_formatted_history()
            
            # Add user message to memory
            self.conversation_memory.add_user_message(user_input)
            
            # Run the agent
            result = self.agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            
            response = result.get("output", "I couldn't generate a response.")
            intermediate_steps = result.get("intermediate_steps", [])
            
            # Add AI response to memory
            self.conversation_memory.add_ai_message(response)
            
            return {
                "response": response,
                "success": True,
                "session_id": self.session_id,
                "intermediate_steps": [
                    {
                        "action": step[0].tool if hasattr(step[0], 'tool') else str(step[0]),
                        "action_input": step[0].tool_input if hasattr(step[0], 'tool_input') else "",
                        "observation": step[1]
                    }
                    for step in intermediate_steps
                ],
                "conversation_summary": self.conversation_memory.get_conversation_summary()
            }
            
        except Exception as e:
            error_message = f"I encountered an error: {str(e)}. Let me try to help you in a different way."
            
            # Add error to memory as well
            self.conversation_memory.add_ai_message(error_message)
            
            return {
                "response": error_message,
                "success": False,
                "error": str(e),
                "session_id": self.session_id
            }
    
    def add_documents_to_memory(self, documents: List, source_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add documents to semantic memory."""
        try:
            from ..utils.file_processor import DocumentProcessor
            
            # Prepare documents for storage
            processed_docs = DocumentProcessor.prepare_documents_for_storage(documents, source_info)
            
            # Add to semantic memory
            doc_ids = self.semantic_memory.add_documents(processed_docs)
            
            return {
                "success": True,
                "doc_ids": doc_ids,
                "count": len(doc_ids),
                "message": f"Successfully added {len(doc_ids)} document chunks to knowledge base."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to add documents to knowledge base: {str(e)}"
            }
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        return {
            "conversation": self.conversation_memory.get_conversation_summary(),
            "semantic_memory": self.semantic_memory.get_stats(),
            "session_id": self.session_id
        }
    
    def clear_conversation_memory(self) -> Dict[str, Any]:
        """Clear conversation memory."""
        try:
            self.conversation_memory.clear_memory()
            return {
                "success": True,
                "message": "Conversation memory cleared successfully."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to clear conversation memory: {str(e)}"
            }
    
    def clear_semantic_memory(self) -> Dict[str, Any]:
        """Clear semantic memory."""
        try:
            self.semantic_memory.clear_memory()
            return {
                "success": True,
                "message": "Knowledge base cleared successfully."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to clear knowledge base: {str(e)}"
            }
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """List documents in semantic memory."""
        try:
            return self.semantic_memory.list_documents()
        except Exception as e:
            return [{"error": str(e)}]
    
    def export_conversation(self) -> Dict[str, Any]:
        """Export conversation history."""
        try:
            return self.conversation_memory.export_conversation()
        except Exception as e:
            return {"error": str(e)}