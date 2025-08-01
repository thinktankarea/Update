import sys
import io
import contextlib
import traceback
from typing import Any, Dict, Optional
from langchain.tools import BaseTool
from pydantic import Field
import ast


class PythonREPLTool(BaseTool):
    """Tool for executing Python code in a safe environment."""
    
    name: str = "python_repl"
    description: str = """
    Execute Python code and return the output. 
    Useful for demonstrating code examples, debugging, and helping students understand programming concepts.
    Input should be valid Python code.
    """
    
    globals_dict: Dict[str, Any] = Field(default_factory=dict)
    
    def _run(self, query: str) -> str:
        """Execute Python code and return the result."""
        try:
            # Parse the code to check for syntax errors
            try:
                ast.parse(query)
            except SyntaxError as e:
                return f"Syntax Error: {str(e)}"
            
            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            # Execute the code
            try:
                # Check if it's an expression or statement
                try:
                    # Try to evaluate as expression first
                    result = eval(query, {"__builtins__": {}}, self.globals_dict)
                    if result is not None:
                        print(result)
                except SyntaxError:
                    # If it fails, execute as statement
                    exec(query, {"__builtins__": {}}, self.globals_dict)
                
            except Exception as e:
                error_traceback = traceback.format_exc()
                return f"Runtime Error: {error_traceback}"
            
            finally:
                sys.stdout = old_stdout
            
            output = captured_output.getvalue()
            return output if output else "Code executed successfully (no output)"
            
        except Exception as e:
            return f"Unexpected Error: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of _run."""
        return self._run(query)
    
    def reset_environment(self):
        """Reset the Python environment."""
        self.globals_dict.clear()
        
    def get_environment_state(self) -> Dict[str, Any]:
        """Get current variables in the environment."""
        return {k: v for k, v in self.globals_dict.items() 
                if not k.startswith('__')}


class SafePythonREPLTool(PythonREPLTool):
    """A safer version of Python REPL that restricts certain operations."""
    
    name: str = "safe_python_repl"
    description: str = """
    Execute Python code in a restricted safe environment.
    Blocks dangerous operations like file system access, network operations, and imports.
    """
    
    BLOCKED_MODULES = {
        'os', 'sys', 'subprocess', 'socket', 'urllib', 'requests',
        'shutil', 'glob', 'tempfile', 'pickle', 'eval', 'exec',
        'open', '__import__'
    }
    
    def _is_safe_code(self, code: str) -> tuple[bool, str]:
        """Check if code is safe to execute."""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        
        for node in ast.walk(tree):
            # Check for dangerous imports
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                module_names = []
                if isinstance(node, ast.Import):
                    module_names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    module_names = [node.module] if node.module else []
                
                for module in module_names:
                    if module and any(blocked in module for blocked in self.BLOCKED_MODULES):
                        return False, f"Blocked import: {module}"
            
            # Check for dangerous function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in self.BLOCKED_MODULES:
                        return False, f"Blocked function call: {node.func.id}"
        
        return True, ""
    
    def _run(self, query: str) -> str:
        """Execute safe Python code."""
        is_safe, reason = self._is_safe_code(query)
        if not is_safe:
            return f"Security Error: {reason}"
        
        return super()._run(query)