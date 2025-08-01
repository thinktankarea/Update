import ast
import re
from typing import Dict, List, Any
from langchain.tools import BaseTool
from pydantic import Field


class ExplainCodeTool(BaseTool):
    """Tool for explaining code snippets and programming concepts."""
    
    name: str = "explain_code"
    description: str = """
    Analyze and explain code snippets in various programming languages.
    Provides detailed explanations of syntax, logic, and best practices.
    Input should be code to analyze.
    """
    
    def _run(self, code: str) -> str:
        """Analyze and explain the provided code."""
        # Detect language
        language = self._detect_language(code)
        
        # Clean and format code
        cleaned_code = self._clean_code(code)
        
        if not cleaned_code.strip():
            return "No code provided to analyze."
        
        # Generate explanation based on language
        if language == "python":
            return self._explain_python_code(cleaned_code)
        elif language == "javascript":
            return self._explain_javascript_code(cleaned_code)
        else:
            return self._explain_generic_code(cleaned_code, language)
    
    async def _arun(self, code: str) -> str:
        """Async version of _run."""
        return self._run(code)
    
    def _detect_language(self, code: str) -> str:
        """Detect the programming language of the code."""
        code_lower = code.lower()
        
        # Python indicators
        python_keywords = ['def ', 'import ', 'from ', 'print(', 'if __name__', 'class ', 'elif ']
        if any(keyword in code_lower for keyword in python_keywords):
            return "python"
        
        # JavaScript indicators  
        js_keywords = ['function', 'var ', 'let ', 'const ', 'console.log', '=>', 'document.']
        if any(keyword in code_lower for keyword in js_keywords):
            return "javascript"
        
        # Java indicators
        java_keywords = ['public class', 'public static void', 'System.out.print']
        if any(keyword in code_lower for keyword in java_keywords):
            return "java"
        
        # C/C++ indicators
        c_keywords = ['#include', 'printf(', 'int main(', 'cout <<']
        if any(keyword in code_lower for keyword in c_keywords):
            return "c/c++"
        
        return "unknown"
    
    def _clean_code(self, code: str) -> str:
        """Clean and format code for analysis."""
        # Remove common markdown code block markers
        code = re.sub(r'^```\w*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'\n```$', '', code, flags=re.MULTILINE)
        
        # Remove excessive whitespace
        lines = code.split('\n')
        cleaned_lines = [line.rstrip() for line in lines]
        
        return '\n'.join(cleaned_lines)
    
    def _explain_python_code(self, code: str) -> str:
        """Provide detailed explanation for Python code."""
        explanation = ["**Python Code Analysis:**\n"]
        
        try:
            # Parse the AST
            tree = ast.parse(code)
            
            # Analyze different code elements
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    explanation.append(f"📦 **Function Definition**: `{node.name}`")
                    explanation.append(f"   - Parameters: {[arg.arg for arg in node.args.args]}")
                    
                elif isinstance(node, ast.ClassDef):
                    explanation.append(f"🏗️ **Class Definition**: `{node.name}`")
                    
                elif isinstance(node, ast.Import):
                    modules = [alias.name for alias in node.names]
                    explanation.append(f"📥 **Import Statement**: {', '.join(modules)}")
                    
                elif isinstance(node, ast.ImportFrom):
                    explanation.append(f"📥 **From Import**: `{node.module}`")
            
            # Add code structure analysis
            explanation.append("\n**Code Structure:**")
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    explanation.append(f"Line {i}: {self._explain_python_line(line)}")
            
        except SyntaxError as e:
            explanation.append(f"⚠️ **Syntax Error**: {str(e)}")
            explanation.append("The code contains syntax errors that prevent proper analysis.")
        
        except Exception as e:
            explanation.append(f"⚠️ **Analysis Error**: {str(e)}")
        
        # Add best practices
        explanation.append("\n**Best Practices Check:**")
        explanation.extend(self._check_python_best_practices(code))
        
        return '\n'.join(explanation)
    
    def _explain_python_line(self, line: str) -> str:
        """Explain a single line of Python code."""
        line = line.strip()
        
        if line.startswith('def '):
            return "Function definition"
        elif line.startswith('class '):
            return "Class definition"
        elif line.startswith('import ') or line.startswith('from '):
            return "Import statement"
        elif line.startswith('if '):
            return "Conditional statement"
        elif line.startswith('for ') or line.startswith('while '):
            return "Loop statement"
        elif line.startswith('try:'):
            return "Exception handling block"
        elif line.startswith('except'):
            return "Exception handler"
        elif '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=']):
            return "Variable assignment"
        elif line.startswith('print('):
            return "Print statement - outputs to console"
        elif line.startswith('return '):
            return "Return statement - exits function with value"
        else:
            return "Code execution"
    
    def _check_python_best_practices(self, code: str) -> List[str]:
        """Check Python code against common best practices."""
        suggestions = []
        
        # Check for proper naming
        if re.search(r'def [A-Z]', code):
            suggestions.append("⚠️ Function names should use snake_case (lowercase with underscores)")
        
        # Check for docstrings
        if 'def ' in code and '"""' not in code and "'''" not in code:
            suggestions.append("💡 Consider adding docstrings to functions for better documentation")
        
        # Check for magic numbers
        numbers = re.findall(r'\b\d{2,}\b', code)
        if numbers:
            suggestions.append("💡 Consider using named constants for magic numbers")
        
        # Check for proper exception handling
        if 'except:' in code:
            suggestions.append("⚠️ Avoid bare except clauses, specify exception types")
        
        if not suggestions:
            suggestions.append("✅ Code follows good Python practices!")
        
        return suggestions
    
    def _explain_javascript_code(self, code: str) -> str:
        """Provide detailed explanation for JavaScript code."""
        explanation = ["**JavaScript Code Analysis:**\n"]
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('//'):
                explanation.append(f"Line {i}: {self._explain_js_line(line)}")
        
        # Add best practices
        explanation.append("\n**Best Practices Check:**")
        explanation.extend(self._check_js_best_practices(code))
        
        return '\n'.join(explanation)
    
    def _explain_js_line(self, line: str) -> str:
        """Explain a single line of JavaScript code."""
        line = line.strip()
        
        if line.startswith('function '):
            return "Function declaration"
        elif line.startswith('const ') or line.startswith('let ') or line.startswith('var '):
            return "Variable declaration"
        elif '=>' in line:
            return "Arrow function"
        elif line.startswith('if ('):
            return "Conditional statement"
        elif line.startswith('for (') or line.startswith('while ('):
            return "Loop statement"
        elif 'console.log(' in line:
            return "Console output statement"
        elif line.startswith('return '):
            return "Return statement"
        else:
            return "Code execution"
    
    def _check_js_best_practices(self, code: str) -> List[str]:
        """Check JavaScript code against common best practices."""
        suggestions = []
        
        # Check for var usage
        if 'var ' in code:
            suggestions.append("💡 Consider using 'let' or 'const' instead of 'var'")
        
        # Check for semicolons
        lines = [line.strip() for line in code.split('\n')]
        missing_semicolons = [line for line in lines if line and not line.endswith((';', '{', '}')) and not line.startswith('//')]
        if missing_semicolons:
            suggestions.append("💡 Consider adding semicolons at the end of statements")
        
        # Check for camelCase
        if re.search(r'[a-z]+_[a-z]+', code):
            suggestions.append("💡 JavaScript typically uses camelCase for variable names")
        
        if not suggestions:
            suggestions.append("✅ Code follows good JavaScript practices!")
        
        return suggestions
    
    def _explain_generic_code(self, code: str, language: str) -> str:
        """Provide generic explanation for unknown languages."""
        explanation = [f"**{language.title()} Code Analysis:**\n"]
        
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        explanation.append(f"📊 **Code Statistics:**")
        explanation.append(f"   - Total lines: {len(lines)}")
        explanation.append(f"   - Non-empty lines: {len(non_empty_lines)}")
        
        # Basic structure analysis
        explanation.append(f"\n**Structure Analysis:**")
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith(('#', '//', '/*')):
                explanation.append(f"Line {i}: {line[:50]}{'...' if len(line) > 50 else ''}")
        
        explanation.append(f"\n**General Observations:**")
        explanation.append("- Code appears to be written in " + language)
        explanation.append("- For detailed analysis, please specify the programming language")
        
        return '\n'.join(explanation)