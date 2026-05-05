import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, FileText, CheckCircle, MessageSquare, Loader2, Send } from 'lucide-react';

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export default function App() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [extractedData, setExtractedData] = useState(null);
  const [systemStats, setSystemStats] = useState(null);

  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [querying, setQuerying] = useState(false);

  // Handle Drag and Drop
  const onDrop = async (acceptedFiles) => {
    const selectedFile = acceptedFiles[0];
    if (!selectedFile) return;
    
    setFile(selectedFile);
    setUploading(true);
    setExtractedData(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      
      setExtractedData(response.data.extracted_data);
      setSystemStats({
        textLength: response.data.text_length,
        chunksIndexed: response.data.chunks_indexed
      });
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Failed to process document. Make sure the backend is running.");
    } finally {
      setUploading(false);
    }
  };

const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 
      "application/pdf": [".pdf"],
      "image/jpeg": [".jpg", ".jpeg"],
      "image/png": [".png"]
    },
    multiple: false
  });

  // Handle AI Chat Query
  const handleAskQuestion = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    const newChat = [...chatHistory, { role: "user", text: question }];
    setChatHistory(newChat);
    setQuestion("");
    setQuerying(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/query`, { question: newChat[newChat.length - 1].text });
      setChatHistory([...newChat, { role: "ai", text: response.data.answer }]);
    } catch (error) {
      setChatHistory([...newChat, { role: "ai", text: "Error connecting to AI. Please try again." }]);
    } finally {
      setQuerying(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex items-center space-x-3 pb-6 border-b border-slate-200">
          <div className="bg-blue-600 p-2 rounded-lg"><FileText className="text-white w-6 h-6" /></div>
          <div>
            <h1 className="text-2xl font-bold text-slate-800">AI Document Verification System</h1>
            <p className="text-sm text-slate-500">RAG-Powered KYC & Data Extraction</p>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Left Column: Upload & Data Display */}
          <div className="space-y-6">
            
            {/* Drag & Drop Zone */}
            <div 
              {...getRootProps()} 
              className={`border-2 border-dashed rounded-xl p-10 flex flex-col items-center justify-center cursor-pointer transition-colors ${
                isDragActive ? "border-blue-500 bg-blue-50" : "border-slate-300 hover:border-blue-400 bg-white"
              }`}
            >
              <input {...getInputProps()} />
              {uploading ? (
                <Loader2 className="w-10 h-10 text-blue-500 animate-spin mb-4" />
              ) : (
                <UploadCloud className="w-10 h-10 text-slate-400 mb-4" />
              )}
              <p className="text-center font-medium text-slate-700">
                {uploading ? "Extracting & Vectorizing Document..." : "Drag & drop a PDF here, or click to select"}
              </p>
              <p className="text-xs text-slate-400 mt-2">Powered by Mistral AI & Pinecone</p>
            </div>

            {/* Extracted Data Card */}
            {extractedData && (
              <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <div className="bg-slate-100 p-4 border-b border-slate-200 flex justify-between items-center">
                  <h3 className="font-semibold flex items-center gap-2"><CheckCircle className="w-4 h-4 text-green-500"/> Structured Data</h3>
                  <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-medium">
                    {systemStats?.chunksIndexed} Vectors Stored
                  </span>
                </div>
                <div className="p-4 grid grid-cols-2 gap-4">
                  {Object.entries(extractedData).map(([key, value]) => (
                    <div key={key} className="space-y-1">
                      <span className="text-xs font-semibold text-slate-500 uppercase">{key.replace(/_/g, " ")}</span>
                      <p className="font-medium text-slate-800 bg-slate-50 p-2 rounded border border-slate-100">
                        {value !== "null" && value !== null ? value.toString() : <span className="text-slate-400 italic">Not found</span>}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right Column: AI Chat Interface */}
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col h-[600px]">
            <div className="bg-slate-100 p-4 border-b border-slate-200 flex items-center gap-2">
              <MessageSquare className="w-5 h-5 text-blue-600"/>
              <h3 className="font-semibold">Document Query (RAG)</h3>
            </div>
            
            {/* Chat History */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {chatHistory.length === 0 ? (
                <div className="h-full flex items-center justify-center text-slate-400 text-sm text-center px-8">
                  Upload a document first, then ask questions about its contents. The AI will search the Pinecone database to answer.
                </div>
              ) : (
                chatHistory.map((msg, idx) => (
                  <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                    <div className={`max-w-[80%] p-3 rounded-lg text-sm ${
                      msg.role === "user" ? "bg-blue-600 text-white rounded-br-none" : "bg-slate-100 text-slate-800 rounded-bl-none"
                    }`}>
                      {msg.text}
                    </div>
                  </div>
                ))
              )}
              {querying && (
                <div className="flex justify-start">
                  <div className="bg-slate-100 text-slate-500 p-3 rounded-lg rounded-bl-none text-sm flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin" /> Searching Database...
                  </div>
                </div>
              )}
            </div>

            {/* Chat Input */}
            <form onSubmit={handleAskQuestion} className="p-4 border-t border-slate-200 flex gap-2">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask about the document..."
                className="flex-1 border border-slate-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={querying || !extractedData}
              />
              <button 
                type="submit" 
                disabled={querying || !question.trim() || !extractedData}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>

        </div>
      </div>
    </div>
  );
}