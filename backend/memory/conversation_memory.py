from typing import Dict, Any, List, Optional
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage, HumanMessage, AIMessage
import json
import os
from datetime import datetime


class ConversationMemoryManager:
    """Manages conversation memory with token limit and persistence."""
    
    def __init__(self, max_token_limit: int = 2000, session_id: str = "default"):
        self.max_token_limit = max_token_limit
        self.session_id = session_id
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            max_token_limit=max_token_limit
        )
        self.conversation_history = []
        self._load_session()
    
    def add_user_message(self, message: str) -> None:
        """Add a user message to memory."""
        human_message = HumanMessage(content=message)
        self.memory.chat_memory.add_message(human_message)
        self.conversation_history.append({
            "type": "human",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        self._save_session()
    
    def add_ai_message(self, message: str) -> None:
        """Add an AI message to memory."""
        ai_message = AIMessage(content=message)
        self.memory.chat_memory.add_message(ai_message)
        self.conversation_history.append({
            "type": "ai", 
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        self._save_session()
    
    def get_conversation_history(self) -> List[BaseMessage]:
        """Get the conversation history as LangChain messages."""
        return self.memory.chat_memory.messages
    
    def get_formatted_history(self) -> str:
        """Get conversation history as formatted string."""
        if not self.conversation_history:
            return "No conversation history."
        
        formatted = []
        for entry in self.conversation_history[-10:]:  # Last 10 messages
            role = "Human" if entry["type"] == "human" else "Assistant"
            formatted.append(f"{role}: {entry['content']}")
        
        return "\n".join(formatted)
    
    def clear_memory(self) -> None:
        """Clear all conversation memory."""
        self.memory.clear()
        self.conversation_history.clear()
        self._save_session()
    
    def get_memory_variables(self) -> Dict[str, Any]:
        """Get memory variables for the agent."""
        return self.memory.load_memory_variables({})
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation."""
        if not self.conversation_history:
            return "No conversation to summarize."
        
        total_messages = len(self.conversation_history)
        human_messages = len([m for m in self.conversation_history if m["type"] == "human"])
        ai_messages = len([m for m in self.conversation_history if m["type"] == "ai"])
        
        return f"Conversation Summary: {total_messages} total messages ({human_messages} from user, {ai_messages} from assistant)"
    
    def _save_session(self) -> None:
        """Save session to file."""
        try:
            session_dir = "sessions"
            if not os.path.exists(session_dir):
                os.makedirs(session_dir)
            
            session_file = os.path.join(session_dir, f"{self.session_id}.json")
            session_data = {
                "session_id": self.session_id,
                "conversation_history": self.conversation_history,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save session: {e}")
    
    def _load_session(self) -> None:
        """Load session from file."""
        try:
            session_file = os.path.join("sessions", f"{self.session_id}.json")
            if os.path.exists(session_file):
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                
                self.conversation_history = session_data.get("conversation_history", [])
                
                # Restore messages to LangChain memory
                for entry in self.conversation_history:
                    if entry["type"] == "human":
                        self.memory.chat_memory.add_message(HumanMessage(content=entry["content"]))
                    elif entry["type"] == "ai":
                        self.memory.chat_memory.add_message(AIMessage(content=entry["content"]))
        except Exception as e:
            print(f"Warning: Could not load session: {e}")
    
    def export_conversation(self) -> Dict[str, Any]:
        """Export conversation for external use."""
        return {
            "session_id": self.session_id,
            "conversation_history": self.conversation_history,
            "summary": self.get_conversation_summary(),
            "exported_at": datetime.now().isoformat()
        }