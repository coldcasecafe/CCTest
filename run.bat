@echo off
REM LangGraph Agents Platform - Run Script (Windows)

echo 🤖 Starting LangGraph Agents Platform...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Virtual environment not found. Creating one...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
if not exist "venv\.installed" (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
    echo. > venv\.installed
    echo ✅ Dependencies installed
)

REM Check for .env file
if not exist ".env" (
    echo ⚠️  No .env file found. Creating from template...
    copy .env.example .env
    echo 📝 Please edit .env and add your OpenAI API key
)

REM Run Streamlit
echo.
echo 🚀 Launching Streamlit application...
echo 📍 Open your browser at http://localhost:8501
echo.

streamlit run app.py
