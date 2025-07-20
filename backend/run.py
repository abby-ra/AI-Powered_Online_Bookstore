#!/usr/bin/env python3
"""
Startup script for the AI-Powered Online Bookstore backend
"""
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Load environment variables
load_dotenv()

# Import and run the Flask app
from app import app

if __name__ == '__main__':
    print("Starting AI-Powered Online Bookstore Backend...")
    print(f"Backend directory: {backend_dir}")
    
    # Run the Flask development server
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
