'use client';

import { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Send, 
  Upload, 
  MessageSquare, 
  Code, 
  Search, 
  Brain,
  FileText,
  Trash2,
  Download,
  BookOpen,
  Lightbulb,
  Cpu
} from 'lucide-react';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  intermediateSteps?: any[];
}

interface FileUpload {
  file: File;
  status: 'uploading' | 'completed' | 'error';
  message?: string;
}

export default function CSInstructorPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [files, setFiles] = useState<FileUpload[]>([]);
  const [memoryStats, setMemoryStats] = useState<any>(null);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

  useEffect(() => {
    // Add welcome message
    const welcomeMessage: Message = {
      id: 'welcome',
      content: `Hello! I'm your AI-powered CS lab instructor. I can help you with:

🐍 **Python Programming** - Execute code, debug, and explain concepts
💻 **Code Analysis** - Analyze and explain code in multiple languages  
🔍 **Research** - Search for programming resources and documentation
📚 **Knowledge Base** - Access uploaded lab materials and documents

Ask me questions, share code to analyze, or upload lab manuals and PDFs. What would you like to learn today?`,
      role: 'assistant',
      timestamp: new Date()
    };
    setMessages([welcomeMessage]);
    
    // Initialize session
    generateSessionId();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const generateSessionId = () => {
    const id = Math.random().toString(36).substring(2) + Date.now().toString(36);
    setSessionId(id);
    return id;
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage,
      role: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          session_id: sessionId
        })
      });

      const data = await response.json();

      if (data.success) {
        const assistantMessage: Message = {
          id: Date.now().toString() + '_ai',
          content: data.response,
          role: 'assistant',
          timestamp: new Date(),
          intermediateSteps: data.intermediate_steps
        };
        setMessages(prev => [...prev, assistantMessage]);
        
        // Update session ID if new one was created
        if (data.session_id && data.session_id !== sessionId) {
          setSessionId(data.session_id);
        }
      } else {
        throw new Error(data.error || 'Failed to get response');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: Date.now().toString() + '_error',
        content: 'Sorry, I encountered an error. Please try again.',
        role: 'assistant',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(event.target.files || []);
    
    for (const file of selectedFiles) {
      const fileUpload: FileUpload = {
        file,
        status: 'uploading'
      };
      
      setFiles(prev => [...prev, fileUpload]);

      try {
        const formData = new FormData();
        formData.append('file', file);
        if (sessionId) {
          formData.append('session_id', sessionId);
        }

        const response = await fetch(`${API_BASE_URL}/upload`, {
          method: 'POST',
          body: formData
        });

        const data = await response.json();

        setFiles(prev => prev.map(f => 
          f.file === file 
            ? { ...f, status: data.success ? 'completed' : 'error', message: data.message }
            : f
        ));

        if (data.success) {
          const uploadMessage: Message = {
            id: Date.now().toString() + '_upload',
            content: `📄 Uploaded and processed: **${file.name}**\n${data.message}`,
            role: 'assistant',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, uploadMessage]);
        }
      } catch (error) {
        setFiles(prev => prev.map(f => 
          f.file === file 
            ? { ...f, status: 'error', message: 'Upload failed' }
            : f
        ));
      }
    }
  };

  const clearMemory = async (type: 'conversation' | 'semantic') => {
    if (!sessionId) return;

    try {
      const response = await fetch(`${API_BASE_URL}/memory/clear`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          type
        })
      });

      const data = await response.json();
      
      if (data.success) {
        if (type === 'conversation') {
          setMessages([]);
        }
        alert(data.message);
      }
    } catch (error) {
      console.error('Error clearing memory:', error);
    }
  };

  const formatMessage = (content: string) => {
    // Simple markdown formatting
    const formatted = content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/```([\s\S]*?)```/g, '<pre class="bg-gray-100 p-2 rounded mt-2 mb-2 overflow-x-auto"><code>$1</code></pre>')
      .replace(/`(.*?)`/g, '<code class="bg-gray-100 px-1 rounded">$1</code>')
      .replace(/\n/g, '<br>');
    
    return { __html: formatted };
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-lg">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">CS Lab Instructor</h1>
                <p className="text-sm text-gray-600">AI-powered programming assistant</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant="outline" className="text-xs">
                Session: {sessionId?.slice(-6) || 'None'}
              </Badge>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowAdvanced(!showAdvanced)}
              >
                Advanced
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Main Chat Area */}
          <div className="lg:col-span-3">
            <Card className="h-[calc(100vh-200px)] flex flex-col">
              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((message) => (
                  <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[80%] rounded-lg p-3 ${
                      message.role === 'user' 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-100 text-gray-900'
                    }`}>
                      <div 
                        className="prose prose-sm max-w-none"
                        dangerouslySetInnerHTML={formatMessage(message.content)}
                      />
                      {message.intermediateSteps && message.intermediateSteps.length > 0 && (
                        <details className="mt-2 text-xs opacity-70">
                          <summary className="cursor-pointer">Show reasoning steps</summary>
                          <div className="mt-1 space-y-1">
                            {message.intermediateSteps.map((step, idx) => (
                              <div key={idx} className="border-l-2 border-gray-300 pl-2">
                                <div><strong>Action:</strong> {step.action}</div>
                                <div><strong>Input:</strong> {step.action_input}</div>
                                <div><strong>Result:</strong> {step.observation?.slice(0, 100)}...</div>
                              </div>
                            ))}
                          </div>
                        </details>
                      )}
                      <div className="text-xs opacity-70 mt-1">
                        {message.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 rounded-lg p-3">
                      <div className="flex items-center space-x-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
                        <span className="text-sm text-gray-600">Thinking...</span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input Area */}
              <div className="border-t p-4">
                <div className="flex space-x-2">
                  <div className="flex-1">
                    <Textarea
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="Ask me about programming, share code to analyze, or request help..."
                      className="min-h-[60px] resize-none"
                      disabled={isLoading}
                    />
                  </div>
                  <div className="flex flex-col space-y-2">
                    <Button
                      onClick={sendMessage}
                      disabled={isLoading || !inputMessage.trim()}
                      size="sm"
                    >
                      <Send className="h-4 w-4" />
                    </Button>
                    <Button
                      onClick={() => fileInputRef.current?.click()}
                      variant="outline"
                      size="sm"
                    >
                      <Upload className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  onChange={handleFileUpload}
                  accept=".pdf,.txt,.py,.js,.java,.cpp,.c,.html,.css,.md"
                  className="hidden"
                />
              </div>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-4">
            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center">
                  <Lightbulb className="h-4 w-4 mr-2" />
                  Quick Actions
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="w-full justify-start"
                  onClick={() => setInputMessage("Explain how Python functions work")}
                >
                  <Code className="h-4 w-4 mr-2" />
                  Python Basics
                </Button>
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="w-full justify-start"
                  onClick={() => setInputMessage("Show me a sorting algorithm")}
                >
                  <Cpu className="h-4 w-4 mr-2" />
                  Algorithms
                </Button>
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="w-full justify-start"
                  onClick={() => setInputMessage("Help me debug this code: def factorial(n): return n * factorial(n-1)")}
                >
                  <Search className="h-4 w-4 mr-2" />
                  Debug Code
                </Button>
              </CardContent>
            </Card>

            {/* File Uploads */}
            {files.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm flex items-center">
                    <FileText className="h-4 w-4 mr-2" />
                    Uploaded Files
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  {files.map((fileUpload, idx) => (
                    <div key={idx} className="text-xs">
                      <div className="flex items-center justify-between">
                        <span className="truncate">{fileUpload.file.name}</span>
                        <Badge variant={fileUpload.status === 'completed' ? 'default' : fileUpload.status === 'error' ? 'destructive' : 'secondary'}>
                          {fileUpload.status}
                        </Badge>
                      </div>
                      {fileUpload.message && (
                        <p className="text-gray-600 mt-1">{fileUpload.message}</p>
                      )}
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}

            {/* Advanced Controls */}
            {showAdvanced && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm flex items-center">
                    <Brain className="h-4 w-4 mr-2" />
                    Memory Controls
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="w-full justify-start"
                    onClick={() => clearMemory('conversation')}
                  >
                    <MessageSquare className="h-4 w-4 mr-2" />
                    Clear Chat
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="w-full justify-start"
                    onClick={() => clearMemory('semantic')}
                  >
                    <Trash2 className="h-4 w-4 mr-2" />
                    Clear Knowledge Base
                  </Button>
                </CardContent>
              </Card>
            )}

            {/* Features */}
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center">
                  <BookOpen className="h-4 w-4 mr-2" />
                  Features
                </CardTitle>
              </CardHeader>
              <CardContent className="text-xs space-y-2">
                <div className="flex items-center space-x-2">
                  <Code className="h-3 w-3 text-green-600" />
                  <span>Python code execution</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Search className="h-3 w-3 text-blue-600" />
                  <span>Web search for resources</span>
                </div>
                <div className="flex items-center space-x-2">
                  <FileText className="h-3 w-3 text-purple-600" />
                  <span>PDF & code file analysis</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Brain className="h-3 w-3 text-orange-600" />
                  <span>Persistent memory</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}