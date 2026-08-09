"""
WSGI entry point for production
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Create application
application = create_app()

if __name__ == '__main__':
    application.run()