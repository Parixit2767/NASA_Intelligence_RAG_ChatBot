# NASA Intelligence RAG ChatBot - Installation Guide

## ⚠️ Windows Installation Notes

This project has a few known Windows-specific issues. The proven working path is:

1. Use Python 3.11+
2. Create a fresh virtual environment
3. Install the core packages first
4. Install `ragas==0.4.3` after the LangChain stack
5. Apply the compatibility patch for newer LangChain imports
6. Build the ChromaDB vector index before starting the app

### Option 1: Safe Windows Setup (Recommended)
```powershell
cd "C:\Users\YourUser\UDACITY_Projects\NASA_Intelligence_RAG_ChatBot"

python -m venv .venv
. .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip setuptools wheel
python -m pip install openai==2.31.0 chromadb==1.5.7 pandas==2.3.3 streamlit==1.56.0
python -m pip install langchain-openai==1.1.13 langchain-google-vertexai==3.2.3
python -m pip install ragas==0.4.3 --no-build-isolation
```

### If you hit the `scikit-network` build error
This happens when `ragas==0.4.3` is installed in a broken or incomplete environment and the C++ toolchain is missing.

Install Visual C++ Build Tools:
1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Select "Desktop development with C++"
3. Restart PowerShell and retry the install commands above

### Option 2: Use Conda (Works well on Windows)
```bash
conda create -n nasa-rag python=3.11
conda activate nasa-rag
conda install -c conda-forge chromadb pandas streamlit openai
pip install langchain-openai==1.1.13 langchain-google-vertexai==3.2.3
pip install ragas==0.4.3 --no-build-isolation
```

### Option 3: Install from requirements file
Use this only after the environment is already valid:
```powershell
. .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

> Important: `pip install requirements` is incorrect. The correct command is `pip install -r requirements.txt`.

---

## 📋 Dependencies Breakdown

| Package | Version | Purpose |
|---------|---------|---------|
| openai | 2.31.0 | OpenAI API client |
| chromadb | 1.5.7 | Vector database |
| langchain-openai | 1.1.13 | LangChain OpenAI integration |
| langchain-google-vertexai | 3.2.3 | Vertex AI support |
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

### Step 2: Create a fresh virtual environment
```powershell
cd "C:\Users\YourUser\UDACITY_Projects\NASA_Intelligence_RAG_ChatBot"
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies in the safe order
```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install openai==2.31.0 chromadb==1.5.7 pandas==2.3.3 streamlit==1.56.0
python -m pip install langchain-openai==1.1.13 langchain-google-vertexai==3.2.3
python -m pip install ragas==0.4.3 --no-build-isolation
```

### Step 4: Apply the legacy RAGAS compatibility fix only where needed
This project avoids the discontinued `langchain-community` package. Nonetheless, the installed `ragas==0.4.3` package still includes legacy import paths, so patch the vendored file in the environment:

```powershell
python -c "from pathlib import Path; p = Path('.venv') / 'Lib' / 'site-packages' / 'ragas' / 'llms' / 'base.py'; print(p)"
```

Then update the imports from:
```python
from langchain_community.chat_models.vertexai import ChatVertexAI
from langchain_community.llms import VertexAI
```

to:
```python
from langchain_google_vertexai import ChatVertexAI
from langchain_google_vertexai import VertexAI
```

### Step 5: Verify Installation
```powershell
python -c "from openai import OpenAI; print('✓ OpenAI OK')"
python -c "import chromadb; print('✓ ChromaDB OK')"
python -c "from langchain_openai import ChatOpenAI; print('✓ LangChain OK')"
python -c "import ragas; from ragas.llms import LangchainLLMWrapper; print('✓ RAGAS OK:', ragas.__version__)"
```

### Step 6: Build Embeddings Database
```powershell
$env:OPENAI_API_KEY="your-api-key-here"

python embedding_pipeline.py `
  --openai-key $env:OPENAI_API_KEY `
  --chroma-dir ./chroma_db_openai `
  --chunk-size 500 `
  --chunk-overlap 100 `
  --data-path .
```

### Step 7: Launch Streamlit App
```powershell
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
```powershell
. .\.venv\Scripts\Activate.ps1
python -c "from langchain_google_vertexai import ChatVertexAI, VertexAI; print('Vertex AI imports OK')"
python -c "import ragas; from ragas.llms import LangchainLLMWrapper; print('RAGAS OK:', ragas.__version__)"
```

If the import still fails, patch the installed file at:
```powershell
.venv\Lib\site-packages\ragas\llms\base.py
```

Replace the old imports:
```python
from langchain_community.chat_models.vertexai import ChatVertexAI
from langchain_community.llms import VertexAI
```

with:
```python
from langchain_google_vertexai import ChatVertexAI
from langchain_google_vertexai import VertexAI
```

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

- [ ] Python 3.11+ installed
- [ ] Fresh virtual environment created
- [ ] Core dependencies installed in the safe order
- [ ] `ragas` import works
- [ ] VertexAI compatibility fix applied
- [ ] OpenAI API key set as environment variable
- [ ] ChromaDB index can be built successfully
- [ ] Streamlit app launches without import errors
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
