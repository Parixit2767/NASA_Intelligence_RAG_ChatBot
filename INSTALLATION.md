# NASA Intelligence RAG ChatBot - Installation Guide

## ⚠️ Windows Installation Notes

If you encounter `Microsoft Visual C++ 14.0 or greater is required` error, use one of these solutions:

### Option 1: Install Visual C++ Build Tools (Recommended)
1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Run installer and select "Desktop development with C++"
3. Restart and retry: `pip install -r requirements.txt`

### Option 2: Use Pre-built Wheels (Faster)
```bash
# Install core dependencies first
pip install openai==2.31.0 chromadb==1.5.7 pandas==2.3.3 streamlit==1.56.0

# Install LangChain dependencies
pip install langchain-openai==1.1.13 langchain-community==0.4.2

# Install RAGAS with specific version
pip install ragas==0.4.3 --no-build-isolation

# Install remaining dependencies
pip install chromadb==1.5.7
```

### Option 3: Use Conda (Easiest for Windows)
```bash
conda create -n nasa-rag python=3.11
conda activate nasa-rag
conda install -c conda-forge chromadb pandas streamlit openai
pip install ragas==0.4.3 langchain-openai==1.1.13 langchain-google-vertexai==3.2.3
```

---

## 📋 Dependencies Breakdown

| Package | Version | Purpose |
|---------|---------|---------|
| openai | 2.31.0 | OpenAI API client |
| chromadb | 1.5.7 | Vector database |
| langchain-openai | 1.1.13 | LangChain OpenAI integration |
| langchain-google-vertexai | 3.2.3 | Vertex AI support |
| langchain-community | 0.4.2 | LangChain community tools |
| ragas | 0.4.3 | RAG evaluation framework |
| pandas | 2.3.3 | Data manipulation |
| streamlit | 1.56.0 | Web UI framework |

---

## 🚀 Complete Installation Steps (Windows)

### Step 1: Set OpenAI API Key
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

Or permanently (add to System Environment Variables):
1. Press `Win + X` → System
2. Advanced system settings → Environment Variables
3. New → Variable name: `OPENAI_API_KEY`
4. Variable value: `your-key-here`

### Step 2: Install Using Option 2 (Recommended for Windows)
```bash
cd NASA_Intelligence_RAG_ChatBot
pip install openai==2.31.0 chromadb==1.5.7 pandas==2.3.3 streamlit==1.56.0
pip install langchain-openai==1.1.13 langchain-community==0.4.2
pip install ragas==0.4.3 --no-build-isolation
```

### Step 3: Verify Installation
```bash
python -c "from openai import OpenAI; print('✓ OpenAI OK')"
python -c "import chromadb; print('✓ ChromaDB OK')"
python -c "from langchain_openai import ChatOpenAI; print('✓ LangChain OK')"
python -c "from ragas import evaluate; print('✓ RAGAS OK')"
```

### Step 4: Build Embeddings Database
```bash
python embedding_pipeline.py `
  --openai-key $env:OPENAI_API_KEY `
  --chroma-dir ./chroma_db_openai `
  --chunk-size 500 `
  --chunk-overlap 100 `
  --data-path .
```

### Step 5: Launch Streamlit App
```bash
streamlit run chat.py
```

This will open: http://localhost:8501

---

## 🔍 Troubleshooting

### ImportError: No module named 'chromadb'
```bash
pip install --upgrade chromadb
```

### RAGAS Import Errors (VertexAI)
See README.md - RAGAS 0.4.3 VertexAI Import Compatibility Fix

### OpenAI API Key Not Found
```powershell
# Check if set
$env:OPENAI_API_KEY

# Set if empty
$env:OPENAI_API_KEY="sk-..."

# Verify
python -c "import os; print(os.getenv('OPENAI_API_KEY')[:10])"
```

### Streamlit Port Already in Use
```bash
streamlit run chat.py --server.port 8502
```

### ChromaDB Persistent Directory Issues
```bash
# Remove old database
Remove-Item -Path ./chroma_db_openai -Recurse -Force

# Rebuild
python embedding_pipeline.py --openai-key $env:OPENAI_API_KEY --chroma-dir ./chroma_db_openai
```

---

## 💡 Pro Tips

1. **Test individual modules first:**
   ```bash
   python test_implementations.py
   ```

2. **Check embedding pipeline status:**
   ```bash
   python embedding_pipeline.py --stats-only --chroma-dir ./chroma_db_openai --openai-key $env:OPENAI_API_KEY
   ```

3. **Adjust chunk parameters for better results:**
   - Small chunks (200-300): More precise retrieval, more API calls
   - Large chunks (1000+): Fewer API calls, less precise
   - Overlap: 10-20% of chunk_size recommended

4. **Monitor API costs:**
   - Embeddings: ~$0.02 per 1M tokens (text-embedding-3-small)
   - Chat: ~$0.0005 per 1K tokens (gpt-3.5-turbo)
   - Evaluation: ~$0.001 per sample (depends on context size)

---

## 📊 Estimated Resource Requirements

| Component | Size | Time | Cost |
|-----------|------|------|------|
| NASA Text Data | ~50 MB | - | - |
| Embeddings Database | ~100 MB | 2-5 min | $0.10-0.20 |
| ChromaDB Index | ~50 MB | - | - |
| Single Query | - | 1-3 sec | $0.002 |
| With Evaluation | - | 3-5 sec | $0.005 |

---

## ✅ Installation Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created (optional but recommended)
- [ ] `pip install` completed successfully
- [ ] OpenAI API key set as environment variable
- [ ] Test imports pass
- [ ] Can access data_text directory with mission files
- [ ] Ready to run embedding pipeline

---

## 📞 Support

If you encounter issues:
1. Check error message against troubleshooting section
2. Review README.md for RAGAS compatibility notes
3. Verify all packages with: `pip list`
4. Check OpenAI API key: `echo $env:OPENAI_API_KEY`
5. Review logs in terminal output

---

**Next Step:** Follow "Complete Installation Steps" above, then proceed to "Running the System" in IMPLEMENTATION_SUMMARY.md
