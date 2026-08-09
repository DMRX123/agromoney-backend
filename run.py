#!/usr/bin/env python3
"""
Application entry point
"""
import os
import sys
from datetime import datetime
from app import create_app
from app.scripts.init_db import init_database

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create application
app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("🌾 MP Mandi Price API")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Environment: {app.config.get('ENVIRONMENT', 'development')}")
    print(f"🗄️  Database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///mp_mandi.db')}")
    print("=" * 60)
    print("📚 API Documentation: http://localhost:5000/api/docs")
    print("❤️  Health Check: http://localhost:5000/health")
    print("=" * 60)

    # Initialize database
    with app.app_context():
        init_database()

    # Run app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config.get('DEBUG', True)
    )