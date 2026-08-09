"""
Seed data script - Add marketplace listings
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app, db
from app.models import User, PriceData, MarketProduct, Notification
import json
from datetime import datetime, timedelta
import random


def seed_data():
    """Seed additional data"""
    app = create_app()

    with app.app_context():
        print("🌱 Seeding additional data...")

        # Create admin if not exists
        admin = User.query.filter_by(phone='9999999999').first()
        if not admin:
            admin = User(
                name='Admin',
                phone='9999999999',
                email='admin@agromoney.in',
                is_admin=True,
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created")

        # Get first user for listing ownership
        first_user = User.query.first()
        if not first_user:
            print("❌ No users found. Please run init_db.py first.")
            return

        print(f"✅ Using user: {first_user.name} (ID: {first_user.id})")

        # ✅ ADD SAMPLE MARKETPLACE LISTINGS
        print("📦 Adding marketplace listings...")

        # Check if listings already exist
        existing_count = MarketProduct.query.count()
        if existing_count > 0:
            print(f"⚠️ {existing_count} listings already exist. Skipping.")
            return

        # Define sample listings
        listings = [
            {
                'user_id': first_user.id,
                'crop': 'Wheat',
                'variety': 'Sharbati',
                'quantity': 50.0,
                'price_per_unit': 2200.0,
                'district': 'Indore',
                'mandi': 'Indore Main Mandi',
                'description': 'Premium quality Sharbati wheat. Best for chapati and bread.',
                'description_hindi': 'प्रीमियम गुणवत्ता शरबती गेहूं। चपाती और ब्रेड के लिए सर्वश्रेष्ठ।',
                'contact_number': '9876543210',
                'status': 'available',
                'is_verified': True,
            },
            {
                'user_id': first_user.id,
                'crop': 'Soybean',
                'variety': 'JS 335',
                'quantity': 40.0,
                'price_per_unit': 3500.0,
                'district': 'Dewas',
                'mandi': 'Dewas Main Mandi',
                'description': 'High yielding soybean variety JS 335. Oil content 18-20%.',
                'description_hindi': 'उच्च उपज सोयाबीन किस्म JS 335। तेल सामग्री 18-20%।',
                'contact_number': '9876543211',
                'status': 'available',
                'is_verified': True,
            },
            {
                'user_id': first_user.id,
                'crop': 'Garlic',
                'variety': 'Local',
                'quantity': 15.0,
                'price_per_unit': 2800.0,
                'district': 'Ratlam',
                'mandi': 'Ratlam Main Mandi',
                'description': 'Fresh local garlic. Strong flavor. Good for medicinal use.',
                'description_hindi': 'ताजा स्थानीय लहसुन। तेज स्वाद। औषधीय उपयोग के लिए अच्छा।',
                'contact_number': '9876543212',
                'status': 'available',
                'is_verified': False,
            },
            {
                'user_id': first_user.id,
                'crop': 'Coriander',
                'variety': 'Local',
                'quantity': 10.0,
                'price_per_unit': 4500.0,
                'district': 'Mandsaur',
                'mandi': 'Mandsaur Main Mandi',
                'description': 'Fresh coriander seeds. High quality for spice and culinary use.',
                'description_hindi': 'ताजा धनिया बीज। मसाले और पाक कला के लिए उच्च गुणवत्ता।',
                'contact_number': '9876543213',
                'status': 'available',
                'is_verified': False,
            },
            {
                'user_id': first_user.id,
                'crop': 'Onion',
                'variety': 'Red',
                'quantity': 30.0,
                'price_per_unit': 1800.0,
                'district': 'Neemuch',
                'mandi': 'Neemuch Main Mandi',
                'description': 'Fresh red onions. Good for cooking and storage. Size 25-35mm.',
                'description_hindi': 'ताजा लाल प्याज। खाना पकाने और भंडारण के लिए अच्छा। आकार 25-35 मिमी।',
                'contact_number': '9876543214',
                'status': 'available',
                'is_verified': True,
            },
            {
                'user_id': first_user.id,
                'crop': 'Gram',
                'variety': 'Chickpea',
                'quantity': 20.0,
                'price_per_unit': 4200.0,
                'district': 'Dhar',
                'mandi': 'Dhar Main Mandi',
                'description': 'High quality chickpeas. Protein rich. Best for dal and cooking.',
                'description_hindi': 'उच्च गुणवत्ता चने। प्रोटीन युक्त। दाल और खाना पकाने के लिए सर्वश्रेष्ठ।',
                'contact_number': '9876543215',
                'status': 'available',
                'is_verified': False,
            },
            {
                'user_id': first_user.id,
                'crop': 'Tomato',
                'variety': 'Roma',
                'quantity': 100.0,
                'price_per_unit': 1500.0,
                'district': 'Ujjain',
                'mandi': 'Ujjain Main Mandi',
                'description': 'Roma tomatoes. Good for sauce and paste. Firm and meaty.',
                'description_hindi': 'रोमा टमाटर। सॉस और पेस्ट के लिए अच्छा। फर्म और मांसल।',
                'contact_number': '9876543216',
                'status': 'available',
                'is_verified': True,
            },
            {
                'user_id': first_user.id,
                'crop': 'Fenugreek',
                'variety': 'Local',
                'quantity': 8.0,
                'price_per_unit': 3800.0,
                'district': 'Indore',
                'mandi': 'Indore Main Mandi',
                'description': 'Fresh fenugreek seeds. Good for medicinal and culinary use.',
                'description_hindi': 'ताजा मेथी बीज। औषधीय और पाक कला के लिए अच्छा।',
                'contact_number': '9876543217',
                'status': 'available',
                'is_verified': False,
            },
            {
                'user_id': first_user.id,
                'crop': 'Peas',
                'variety': 'Green',
                'quantity': 25.0,
                'price_per_unit': 3200.0,
                'district': 'Dewas',
                'mandi': 'Dewas Main Mandi',
                'description': 'Fresh green peas. Sweet and tender. Best for vegetables.',
                'description_hindi': 'ताजी हरी मटर। मीठी और कोमल। सब्जियों के लिए सर्वश्रेष्ठ।',
                'contact_number': '9876543218',
                'status': 'available',
                'is_verified': True,
            }
        ]

        # Add all listings
        for listing_data in listings:
            # Check if listing already exists (by crop + district + user)
            existing = MarketProduct.query.filter_by(
                crop=listing_data['crop'],
                district=listing_data['district'],
                user_id=listing_data['user_id']
            ).first()
            
            if not existing:
                listing = MarketProduct(**listing_data)
                db.session.add(listing)

        db.session.commit()
        
        total_listings = MarketProduct.query.count()
        print(f"✅ Created {len(listings)} marketplace listings")
        print(f"📊 Total listings in database: {total_listings}")

        # ✅ Also add a few sold listings for testing
        sold_listings = [
            {
                'user_id': first_user.id,
                'crop': 'Wheat',
                'variety': 'Local',
                'quantity': 20.0,
                'price_per_unit': 2100.0,
                'district': 'Bhopal',
                'mandi': 'Bhopal Main Mandi',
                'description': 'Local wheat variety. Good for daily use.',
                'description_hindi': 'स्थानीय गेहूं किस्म। दैनिक उपयोग के लिए अच्छा।',
                'contact_number': '9876543216',
                'status': 'sold',
                'is_verified': True,
                'created_at': datetime.now() - timedelta(days=10)
            },
            {
                'user_id': first_user.id,
                'crop': 'Onion',
                'variety': 'White',
                'quantity': 10.0,
                'price_per_unit': 2000.0,
                'district': 'Indore',
                'mandi': 'Indore Main Mandi',
                'description': 'White onions. Mild flavor. Good for salads.',
                'description_hindi': 'सफेद प्याज। हल्का स्वाद। सलाद के लिए अच्छा।',
                'contact_number': '9876543217',
                'status': 'sold',
                'is_verified': True,
                'created_at': datetime.now() - timedelta(days=15)
            }
        ]

        for listing_data in sold_listings:
            existing = MarketProduct.query.filter_by(
                crop=listing_data['crop'],
                district=listing_data['district'],
                user_id=listing_data['user_id'],
                status='sold'
            ).first()
            
            if not existing:
                listing = MarketProduct(**listing_data)
                db.session.add(listing)

        db.session.commit()
        print(f"✅ Added {len(sold_listings)} sold listings for testing")
        print(f"📊 Total listings (including sold): {MarketProduct.query.count()}")

        print("🎉 Seeding complete!")


if __name__ == '__main__':
    seed_data()