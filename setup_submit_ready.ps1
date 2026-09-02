$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

function Test-CommandExists {
    param([string]$Name)
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    return [bool]$cmd
}

Write-Host "Checking for Python 3.11+..."
$pythonCmd = $null
if (Test-CommandExists "py") {
    foreach ($v in @("3.11", "3.12", "3.10")) {
        $cmd = "py -$v"
        & $cmd -c "import sys; print(sys.version_info[:2])" *> $null
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = $cmd
            break
        }
    }
}

if (-not $pythonCmd -and (Test-CommandExists "python")) {
    & python -c "import sys; print(sys.version_info[:2])" *> $null
    if ($LASTEXITCODE -eq 0) {
        $pythonCmd = "python"
    }
}

if (-not $pythonCmd) {
    Write-Error "Python 3.11+ is required but not found. Install Python 3.11 and rerun this script."
    exit 1
}

Write-Host "Using: $pythonCmd"

if (Test-Path ".\.venv") {
    Write-Host "Removing old virtual environment..."
    Remove-Item -Recurse -Force .venv
}

Write-Host "Creating fresh virtual environment..."
& $pythonCmd -m venv .venv
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

. .\.venv\Scripts\Activate.ps1

Write-Host "Upgrading packaging tools..."
python -m pip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Installing the project dependencies in a safe order..."
python -m pip install openai==2.31.0 chromadb==1.5.7 pandas==2.3.3 streamlit==1.56.0
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -m pip install langchain-openai==1.1.13 langchain-google-vertexai==3.2.3
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -m pip install ragas==0.4.3 --no-build-isolation
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Applying the known RAGAS compatibility fix..."
$p = Join-Path $env:VIRTUAL_ENV "Lib\site-packages\ragas\llms\base.py"
if (Test-Path $p) {
    $content = Get-Content -Path $p -Raw
    $content = $content.Replace("from langchain_community.chat_models.vertexai import ChatVertexAI", "from langchain_google_vertexai import ChatVertexAI")
    $content = $content.Replace("from langchain_community.llms import VertexAI", "from langchain_google_vertexai import VertexAI")
    Set-Content -Path $p -Value $content
}

Write-Host "Verifying imports..."
python -c "import chromadb, ragas; from ragas.llms import LangchainLLMWrapper; print('chromadb ok'); print('ragas', ragas.__version__)"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Environment setup complete."
Write-Host "Next:"
Write-Host "  $env:OPENAI_API_KEY='your-key'"
Write-Host "  python embedding_pipeline.py --data-path . --openai-key $env:OPENAI_API_KEY --chroma-dir ./chroma_db_openai --chunk-size 500 --chunk-overlap 100 --update-mode skip"
Write-Host "  streamlit run chat.py"
