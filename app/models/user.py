"""
User model
"""
from datetime import datetime
from app import db
from flask_jwt_extended import create_access_token, create_refresh_token
import json


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    district = db.Column(db.String(100), index=True)
    village = db.Column(db.String(100))
    land_area = db.Column(db.Float)
    soil_type = db.Column(db.String(100))
    language = db.Column(db.String(10), default='hindi')
    crops_grown = db.Column(db.Text)  # JSON string
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relationships - ✅ FIX: Use foreign_keys
    market_products = db.relationship('MarketProduct', foreign_keys='MarketProduct.user_id', back_populates='user', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', back_populates='user', cascade='all, delete-orphan')

    def __init__(self, name, phone, **kwargs):
        self.name = name
        self.phone = phone
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self, language='english'):
        crops = []
        if self.crops_grown:
            try:
                crops = json.loads(self.crops_grown)
            except:
                crops = []

        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'district': self.district,
            'village': self.village,
            'land_area': self.land_area,
            'soil_type': self.soil_type,
            'language': self.language,
            'crops_grown': crops,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

    def generate_tokens(self):
        access_token = create_access_token(identity=str(self.id))
        refresh_token = create_refresh_token(identity=str(self.id))
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    @classmethod
    def get_by_phone(cls, phone):
        """Get user by phone number"""
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def get_by_email(cls, email):
        """Get user by email"""
        return cls.query.filter_by(email=email).first()

    def add_crop(self, crop):
        """Add a crop to user's grown crops"""
        crops = []
        if self.crops_grown:
            try:
                crops = json.loads(self.crops_grown)
            except:
                crops = []
        if crop not in crops:
            crops.append(crop)
            self.crops_grown = json.dumps(crops)
            db.session.commit()

    def remove_crop(self, crop):
        """Remove a crop from user's grown crops"""
        crops = []
        if self.crops_grown:
            try:
                crops = json.loads(self.crops_grown)
            except:
                crops = []
        if crop in crops:
            crops.remove(crop)
            self.crops_grown = json.dumps(crops)
            db.session.commit()

    def get_crops(self):
        """Get list of user's crops"""
        if self.crops_grown:
            try:
                return json.loads(self.crops_grown)
            except:
                return []
        return []

    def __repr__(self):
        return f'<User {self.name} - {self.phone}>'