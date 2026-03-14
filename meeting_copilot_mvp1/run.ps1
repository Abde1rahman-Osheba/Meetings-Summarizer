param(
  [switch]$InstallDeps
)

$ErrorActionPreference = "Stop"

if (!(Test-Path ".venv")) {
  python -m venv .venv
}

.\.venv\Scripts\Activate.ps1

if ($InstallDeps) {
  pip install --upgrade pip
  pip install -r requirements.txt
}

if (!(Test-Path ".env")) {
  Copy-Item .env.example .env
}

$env:PYTHONPATH = "."
streamlit run ui/streamlit_app.py
