"""
Market Product model for marketplace listings
"""
from datetime import datetime
from app import db


class MarketProduct(db.Model):
    __tablename__ = 'market_products'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    crop = db.Column(db.String(100), nullable=False, index=True)
    variety = db.Column(db.String(100))
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='quintal')
    price_per_unit = db.Column(db.Float)
    district = db.Column(db.String(100), index=True)
    mandi = db.Column(db.String(100), index=True)
    village = db.Column(db.String(100))
    description = db.Column(db.Text)
    description_hindi = db.Column(db.Text)
    contact_number = db.Column(db.String(15))
    image_url = db.Column(db.String(500))
    status = db.Column(db.String(20), default='available', index=True)
    is_verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    verified_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships - ✅ FIX: Specify foreign_keys
    user = db.relationship('User', foreign_keys=[user_id], back_populates='market_products')
    verifier = db.relationship('User', foreign_keys=[verified_by])

    def to_dict(self, language='english'):
        base = {
            'id': self.id,
            'user_id': self.user_id,
            'crop': self.crop,
            'variety': self.variety,
            'quantity': self.quantity,
            'unit': self.unit,
            'price_per_unit': self.price_per_unit,
            'district': self.district,
            'mandi': self.mandi,
            'village': self.village,
            'contact_number': self.contact_number,
            'image_url': self.image_url,
            'status': self.status,
            'is_verified': self.is_verified,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        if language == 'hindi' and self.description_hindi:
            base['description'] = self.description_hindi
        else:
            base['description'] = self.description

        return base

    def verify(self, admin_id):
        self.is_verified = True
        self.verified_by = admin_id
        self.verified_at = datetime.utcnow()
        self.status = 'verified'

    def update_status(self, status):
        valid_statuses = ['available', 'sold', 'reserved', 'removed', 'verified']
        if status in valid_statuses:
            self.status = status
            self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f'<MarketProduct {self.crop} - {self.quantity} {self.unit}>'