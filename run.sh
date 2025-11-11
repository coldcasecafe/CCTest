#!/bin/bash

# LangGraph Agents Platform - Run Script

echo "🤖 Starting LangGraph Agents Platform..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
    echo "✅ Dependencies installed"
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env and add your OpenAI API key"
fi

# Run Streamlit
echo ""
echo "🚀 Launching Streamlit application..."
echo "📍 Open your browser at http://localhost:8501"
echo ""

streamlit run app.py
