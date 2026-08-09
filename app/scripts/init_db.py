"""
Database initialization script
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app, db
from app.models import User, PriceData, MarketProduct, Notification
from app.config import Config
import json


def init_database():
    """Initialize database with sample data"""
    app = create_app()

    with app.app_context():
        print("Creating database tables...")
        db.create_all()

        # Check if data exists
        if User.query.count() > 0:
            print("Database already has data. Skipping seeding.")
            return

        print("Seeding initial data...")

        # Create admin user
        admin = User(
            name='Admin',
            phone='9999999999',
            email='admin@agromoney.in',
            district='Bhopal',
            language='english',
            is_admin=True,
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()

        print(f"✅ Created admin user with ID: {admin.id}")

        # Create sample users
        users = [
            {'name': 'Rajesh Kumar', 'phone': '9876543210', 'district': 'Bhopal',
             'crops_grown': json.dumps(['Wheat', 'Soybean'])},
            {'name': 'Suresh Patel', 'phone': '9876543211', 'district': 'Indore',
             'crops_grown': json.dumps(['Onion', 'Garlic'])},
            {'name': 'Mohan Singh', 'phone': '9876543212', 'district': 'Jabalpur',
             'crops_grown': json.dumps(['Wheat', 'Rice'])}
        ]

        for user_data in users:
            user = User(**user_data)
            db.session.add(user)

        db.session.commit()
        print(f"✅ Created {len(users)} sample users")

        crops = [
            'Wheat', 'Rice', 'Soybean', 'Onion', 'Garlic', 'Tomato',
            'Coriander', 'Peas', 'Gram', 'Fenugreek'
        ]
        districts = [
            'Bhopal', 'Indore', 'Jabalpur', 'Gwalior', 'Ujjain',
            'Dewas', 'Ratlam', 'Mandsaur', 'Neemuch', 'Dhar'
        ]

        from datetime import datetime, timedelta
        import random

        price_count = 0
        for crop in crops:
            for district in districts:
                for i in range(7):
                    price = PriceData(
                        district=district,
                        mandi=f"{district} Main Mandi",
                        crop=crop,
                        variety="Regular",
                        min_price=1500 + random.randint(0, 1000),
                        max_price=2500 + random.randint(0, 1000),
                        modal_price=2000 + random.randint(0, 800),
                        arrival_date=datetime.now() - timedelta(days=i)
                    )
                    db.session.add(price)
                    price_count += 1

        db.session.commit()
        print(f"✅ Created {price_count} sample price records")

        # Sample notifications
        notifications = [
            {
                'title': 'Welcome to Agromoney',
                'message': 'Welcome to Agromoney platform. Get real-time mandi prices and market updates.',
                'notification_type': 'general',
                'is_sent': True,
                'sent_at': datetime.utcnow()
            },
            {
                'title': 'Wheat Price Update',
                'message': 'Wheat prices have increased by 5% in Bhopal mandi.',
                'notification_type': 'price_alert',
                'target_district': 'Bhopal',
                'target_crop': 'Wheat',
                'is_sent': True,
                'sent_at': datetime.utcnow()
            }
        ]

        for notif_data in notifications:
            notification = Notification(**notif_data)
            db.session.add(notification)

        db.session.commit()
        print(f"✅ Created {len(notifications)} sample notifications")

        print("🎉 Database initialization complete!")


if __name__ == '__main__':
    init_database()