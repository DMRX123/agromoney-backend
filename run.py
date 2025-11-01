#!/usr/bin/env python3
"""
Agromoney Backend Server v2.0
Madhya Pradesh Agriculture Market Analytics
"""

import os
import sys
from app import app

def print_startup_banner():
    """Print startup banner"""
    banner = """
    🚀 AGROMONEY BACKEND SERVER v2.0
    Advanced MP Agriculture Market Analytics
    """
    print(banner)

def print_version_info():
    """Print version highlights"""
    print("\n✨ VERSION 2.0 FEATURES")
    print("   " + "="*40)
    features = [
        "🌐 Enhanced CORS for Flutter Web",
        "📊 10-Year Historical Data Analysis", 
        "🕯️ Advanced Candlestick Charts",
        "🎯 Smart Price Alerts",
        "👥 User Reliability Scoring",
        "🏪 Complete Marketplace",
        "📈 Extended Predictions",
        "🔔 Real-time Notifications"
    ]
    for feature in features:
        print(f"   {feature}")

def print_server_info():
    """Print server configuration"""
    print("\n📋 SERVER CONFIG")
    print("   " + "="*40)
    print(f"   Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"   Debug Mode: {app.config['DEBUG']}")
    print(f"   Districts: {len(app.config['MP_DISTRICTS'])}")
    print(f"   Crops: {len(app.config['CROPS'])}")
    print(f"   Data Period: {app.config.get('HISTORICAL_YEARS', 10)} years")

def print_cors_info():
    """Print CORS configuration"""
    print("\n🌐 CORS CONFIGURATION")
    print("   " + "="*40)
    origins = ["localhost:3000", "localhost:5000", "localhost:8080", "localhost:58916"]
    for origin in origins:
        print(f"   ✅ http://{origin}")
    print("   Methods: GET, POST, PUT, DELETE, OPTIONS")
    print("   Headers: Content-Type, Authorization, Accept")

def print_api_endpoints():
    """Print main API endpoints"""
    print("\n🌐 MAIN ENDPOINTS")
    print("   " + "="*40)
    
    endpoints = {
        "Market Data": [
            "GET  /api/market/rates?crop=Wheat",
            "GET  /api/market/historical?crop=Wheat&years=10", 
            "GET  /api/market/candle-data?crop=Tomato",
            "GET  /api/market/crops",
            "GET  /api/market/districts"
        ],
        "Analysis": [
            "GET  /api/analysis/trends?crop=Wheat",
            "GET  /api/analysis/market-prediction?crop=Tomato",
            "GET  /api/analysis/crop-insights?crop=Wheat",
            "GET  /api/analysis/weather-analysis?crop=Wheat",
            "GET  /api/analysis/crop-recommendation?district=Indore"
        ],
        "User & Marketplace": [
            "POST /api/user/register",
            "GET  /api/user/profile/1", 
            "POST /api/user/listings",
            "GET  /api/user/listings?crop=Wheat",
            "POST /api/user/alerts",
            "GET  /api/user/alerts?user_id=1",
            "GET  /api/user/notifications?user_id=1",
            "POST /api/user/buying-requests"
        ]
    }
    
    for category, routes in endpoints.items():
        print(f"\n   📊 {category}")
        for route in routes:
            print(f"      {route}")

def check_dependencies():
    """Check required dependencies"""
    print("\n🔧 DEPENDENCIES")
    print("   " + "="*40)
    
    dependencies = ['flask', 'flask_cors', 'pandas', 'requests', 'numpy']
    all_ok = True
    
    for package in dependencies:
        try:
            __import__(package)
            print(f"   ✅ {package:15} - OK")
        except ImportError:
            print(f"   ❌ {package:15} - MISSING")
            all_ok = False
    
    return all_ok

def print_quick_tips():
    """Print development tips"""
    print("\n💡 QUICK TIPS")
    print("   " + "="*40)
    tips = [
        "Use years=10 for best historical analysis",
        "Try interval_days=30 for candle charts", 
        "Check confidence_score in predictions",
        "CORS ready for Flutter Web development",
        "All endpoints support OPTIONS preflight",
        "User registration required for marketplace",
        "Price alerts work with user preferences"
    ]
    for tip in tips:
        print(f"   • {tip}")

def print_test_commands():
    """Print test commands for quick verification"""
    print("\n🧪 QUICK TEST COMMANDS")
    print("   " + "="*40)
    commands = [
        "curl http://localhost:5000/api/health",
        "curl http://localhost:5000/api/market/crops",
        "curl 'http://localhost:5000/api/market/rates?crop=Wheat&district=Indore'",
        "curl http://localhost:5000/api/user/listings"
    ]
    for cmd in commands:
        print(f"   $ {cmd}")

def main():
    """Main application entry point"""
    print_startup_banner()
    print_version_info()
    
    if not check_dependencies():
        print("\n⚠️  Install missing dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    print_server_info()
    print_cors_info() 
    print_api_endpoints()
    print_quick_tips()
    print_test_commands()
    
    print("\n🎯 SERVER READY")
    print("   " + "="*40)
    print(f"   🌍 http://localhost:5000")
    print(f"   🌐 http://0.0.0.0:5000")
    print(f"   📚 /api/docs - API Documentation")
    print(f"   🏥 /api/health - Health Check")
    print(f"   📊 /api/stats - Statistics")
    print(f"   🚀 /api/quick-start - Quick Start Guide")
    print("   " + "="*40)
    print("   Starting Flask server...\n")
    
    try:
        app.run(
            debug=app.config['DEBUG'],
            host=os.getenv('HOST', '0.0.0.0'),
            port=int(os.getenv('PORT', 5000)),
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()