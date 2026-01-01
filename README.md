# Research Paper Analysis System

A Flask-based web application that uses AI to analyze research papers, extract sections, generate summaries, and answer questions using RAG (Retrieval Augmented Generation).

![Research Paper Analyzer](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3.27-orange.svg)

## 🎯 Features

- **PDF Upload & Text Extraction**: Upload research papers and extract text using PyMuPDF
- **Section Detection**: Automatically identify paper sections (Abstract, Introduction, Methods, etc.)
- **AI-Powered Summaries**: Generate detailed summaries for each section using Groq LLM
- **RAG Chat Interface**: Ask questions about your paper and get contextual answers
- **Modern Web UI**: Beautiful, responsive interface with gradient backgrounds and animations

## 🏗️ Architecture

### Backend Components

```
app.py                              # Flask application with API endpoints
├── /upload                         # Upload PDF and extract sections
├── /summary                        # Generate AI summaries
└── /chat                           # RAG-based Q&A

src/
├── load_and_extract_text.py        # PDF text extraction (PyMuPDF)
├── detect_and_split_sections.py    # Section detection and filtering
├── get_summary.py                  # LLM-based summary generation
├── create_vector_db.py             # FAISS vector database creation
└── RAG_retrival_chain.py           # RAG chain for Q&A
```

### Frontend

```
templates/
└── index.html                      # Single-page application with:
    ├── Hero section
    ├── Upload interface
    ├── Topic selection dropdown
    ├── Summary display
    └── Chat interface
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Groq API key (free tier available at [console.groq.com](https://console.groq.com))
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Research-Paper-Analysis-Project
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/Mac
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   LLM_MODEL=llama-3.3-70b-versatile
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   ```

   Get your free Groq API key from: https://console.groq.com/keys

5. **Run the application**
   ```bash
   # If using virtual environment in parent directory
   ..\.venv\Scripts\python.exe app.py

   # Or if venv is in project directory
   python app.py
   ```

6. **Open in browser**
   
   Navigate to: `http://localhost:5000`

## 📖 How It Works

### 1. PDF Upload & Processing

```python
# User uploads PDF via web interface
file → saved to uploads/ folder
     → PyMuPDF extracts text
     → Regex patterns detect sections
     → Local filtering removes figures/tables
     → Returns list of topics
```

### 2. Section Detection

The system uses regex patterns to identify common research paper sections:

```python
patterns = [
    r'\b(Abstract|ABSTRACT)\b',
    r'\b(\d+\.?\s*Introduction|INTRODUCTION)\b',
    r'\b(\d+\.?\s*Methods?|METHODS?)\b',
    r'\b(\d+\.?\s*Results?|RESULTS?)\b',
    r'\b(\d+\.?\s*Discussion|DISCUSSION)\b',
    r'\b(\d+\.?\s*Conclusion|CONCLUSION)\b',
    r'\b(References|REFERENCES)\b'
]
```

### 3. Summary Generation

```python
# For each section:
topic_content → LLM prompt with instructions
             → Groq API (llama-3.3-70b-versatile)
             → Structured summary returned
             → Formatted and displayed
```

### 4. RAG Chat System

```python
# On first chat:
full_text → RecursiveCharacterTextSplitter (500 chars, 100 overlap)
         → HuggingFace embeddings (all-MiniLM-L6-v2)
         → FAISS vector database
         → Saved locally

# For each question:
user_question → Similarity search (k=4 chunks)
             → Retrieved context + question → LLM
             → Contextual answer returned
```

## 🔧 Configuration

### Model Selection

You can change the LLM model in `.env`:

```env
# Faster, smaller model (good for free tier)
LLM_MODEL=llama-3.1-8b-instant

# More powerful model (may hit rate limits)
LLM_MODEL=llama-3.3-70b-versatile
```

### Rate Limit Handling

The free Groq tier has a limit of **12,000 tokens per minute**. The system handles this by:

- **Section refinement**: Uses local filtering instead of LLM
- **Summary generation**: Processes one section at a time
- **Chat**: Uses smaller text chunks (500 chars)

If you hit rate limits:
- Wait 1 minute between requests
- Use a smaller model (`llama-3.1-8b-instant`)
- Upgrade to Groq Dev Tier

### Chunk Size Configuration

Adjust in `src/create_vector_db.py`:

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # Increase for more context
    chunk_overlap=100,   # Increase for better continuity
    separators=["\n\n", "\n", ".", " "]
)
```

## 📁 Project Structure

```
Research-Paper-Analysis-Project/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (create this)
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
│
├── src/                           # Backend modules
│   ├── __init__.py
│   ├── load_and_extract_text.py
│   ├── detect_and_split_sections.py
│   ├── get_summary.py
│   ├── create_vector_db.py
│   └── RAG_retrival_chain.py
│
├── templates/                     # Frontend templates
│   └── index.html
│
├── static/                        # Static assets
│   ├── hero2.jpg
│   └── hero3.jpg
│
├── uploads/                       # Uploaded PDFs (created automatically)
│
└── research_paper_vector_db/      # FAISS index (created at runtime)
```

## 🎨 Frontend Features

### Modern UI Design
- Gradient backgrounds and glassmorphism effects
- Smooth animations and hover effects
- Responsive layout (mobile-friendly)
- Professional color scheme

### Interactive Elements
- Drag & drop file upload
- Progress bar during processing
- Dynamic topic dropdown
- Real-time chat interface
- Formatted summary display

## 🔍 API Endpoints

### POST /upload
Upload a PDF and extract sections.

**Request:**
```javascript
FormData {
  file: <PDF file>
}
```

**Response:**
```json
{
  "topics": ["Abstract", "Introduction", "Methods", "Results", "Conclusion"]
}
```

### POST /summary
Generate summary for a specific topic.

**Request:**
```json
{
  "topic": "Introduction"
}
```

**Response:**
```json
{
  "summary": "## Main Idea\nThe paper introduces...\n\n## Key Points\n- Point 1\n- Point 2"
}
```

### POST /chat
Ask questions about the paper.

**Request:**
```json
{
  "message": "What methodology was used?"
}
```

**Response:**
```json
{
  "response": "The study used a mixed-methods approach..."
}
```

## 🛠️ Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
# Make sure you're in the virtual environment
# Windows
.venv\Scripts\activate

# Install missing packages
pip install -r requirements.txt
```

### Issue: Rate limit exceeded (413 error)

**Solution:**
- Wait 60 seconds between requests
- Use smaller model: `LLM_MODEL=llama-3.1-8b-instant`
- Upgrade to Groq Dev Tier

### Issue: Chat returns "I don't know"

**Solution:**
- Make sure you uploaded a PDF first
- Check that the question is related to the paper content
- Try rephrasing your question
- Check server logs for errors

### Issue: PDF upload fails

**Solution:**
- Ensure PDF is not corrupted
- Check file size (very large PDFs may timeout)
- Verify PDF contains extractable text (not just images)

## 🧪 Testing

### Manual Testing Checklist

1. **Upload Test**
   - [ ] Upload a valid PDF
   - [ ] Verify topics appear in dropdown
   - [ ] Check uploads/ folder for saved file

2. **Summary Test**
   - [ ] Select each topic
   - [ ] Verify summary generates
   - [ ] Check formatting (headings, bullets)

3. **Chat Test**
   - [ ] Ask a question about the paper
   - [ ] Verify relevant answer
   - [ ] Test multiple questions
   - [ ] Check chat history displays correctly

### Automated Testing

Run the backend test script:
```bash
python test_backend.py
```

This verifies:
- Environment variables
- LLM connection
- Embeddings model
- All custom modules

## 📊 Performance Optimization

### For Large PDFs
- Increase chunk size to reduce number of chunks
- Use faster model for summaries
- Implement caching for repeated queries

### For Production
- Use production WSGI server (Gunicorn/uWSGI)
- Add Redis for session management
- Implement database for persistence
- Add rate limiting middleware
- Use CDN for static assets

## 🔐 Security Considerations

- **Never commit `.env` file** (already in `.gitignore`)
- Store API keys securely
- Validate file uploads (type, size)
- Sanitize user inputs
- Add CORS configuration for production
- Implement authentication if needed

## 📝 Dependencies

### Core
- `Flask==3.1.2` - Web framework
- `python-dotenv==1.1.1` - Environment variables
- `PyMuPDF==1.26.4` - PDF text extraction

### AI/ML
- `langchain==0.3.27` - LLM orchestration
- `langchain-groq==0.3.8` - Groq integration
- `langchain-huggingface==0.3.1` - HuggingFace embeddings
- `langchain-community==0.3.30` - Community integrations
- `sentence-transformers==5.1.1` - Embedding models
- `faiss-cpu==1.10.0` - Vector database

See `requirements.txt` for complete list.

