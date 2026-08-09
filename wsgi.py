"""
WSGI entry point for production servers (Gunicorn)
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Create application instance for WSGI servers
app = create_app()

# For Gunicorn
if __name__ == "__main__":
    app.run()