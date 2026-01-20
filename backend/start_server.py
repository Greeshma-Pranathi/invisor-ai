#!/usr/bin/env python3
"""
Startup script for Invisor.ai Backend
"""

import uvicorn
import os
import sys
from pathlib import Path

def main():
    """Start the FastAPI server"""
    
    # Set default environment variables if not set
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    print("=" * 50)
    print("🚀 Starting Invisor.ai Backend Server")
    print("=" * 50)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Environment: {'Production' if os.getenv('ENVIRONMENT') == 'production' else 'Development'}")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Warning: .env file not found. Using default configuration.")
        print("   Copy .env.example to .env and configure your settings.")
        print()
    
    # Start the server
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=True,  # Enable auto-reload for development
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()