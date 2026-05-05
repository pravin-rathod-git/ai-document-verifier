# 🚀 AI Document Verification System (RAG-Powered)

<div align="center">
  
  [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![Mistral AI](https://img.shields.io/badge/Mistral_AI-F54E4E?style=for-the-badge&logo=mistral&logoColor=white)](https://mistral.ai/)
  [![Pinecone](https://img.shields.io/badge/Pinecone-000000?style=for-the-badge&logo=pinecone&logoColor=white)](https://www.pinecone.io/)
  [![LangChain](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://python.langchain.com/)

  *An enterprise-grade, multimodal Know Your Customer (KYC) and document auditing platform.*
</div>

---


---

## 🧠 Core Architecture

This application simulates a real-world immigration or financial KYC workflow. It accepts multimodal documents (PDFs and Scans), extracts strict schema-valid data to prevent AI hallucination, and utilizes an autonomous LangGraph agent for conversational auditing.

### ✨ Key Features
* **Multimodal Ingestion:** Dynamically routes PDFs to `PyPDF` and Scans/Images to `Tesseract OCR` for robust text extraction.
* **Zero-Hallucination Extraction:** Utilizes Mistral AI's `with_structured_output` bound to strict Pydantic schemas to ensure predictable, application-ready JSON.
* **Serverless Vector Storage:** Seamlessly integrates with Pinecone for dense vector embeddings and high-speed semantic search.
* **Agentic Routing & Memory:** Powered by LangGraph. The backend operates as an autonomous agent that maintains conversational state (`Checkpointer`) and autonomously decides when to trigger the Pinecone search Tool.
* **Modern Interface:** A responsive, drag-and-drop dashboard built with React, Vite, and Tailwind CSS.

---

## 🏗️ Folder Structure

```text
ai-doc-verifier/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI REST endpoints (Upload, Query)
│   │   ├── core/         # Mistral LLM Configuration & Pydantic Schemas
│   │   ├── db/           # Pinecone Vector Store initialization
│   │   └── services/     # LangGraph Agent, OCR Parsers, RAG logic
│   ├── main.py           # Uvicorn entry point
│   └── requirements.txt  # Managed via `uv`
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Main Dashboard UI
│   │   └── index.css     # Tailwind Directives
│   ├── tailwind.config.js
│   └── package.json
└── README.md
