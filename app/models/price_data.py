"""
Price Data model
"""
from datetime import datetime
from app import db


class PriceData(db.Model):
    __tablename__ = 'price_data'

    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.String(100), nullable=False, index=True)
    mandi = db.Column(db.String(100), nullable=False, index=True)
    crop = db.Column(db.String(100), nullable=False, index=True)
    variety = db.Column(db.String(100))
    grade = db.Column(db.String(50))
    min_price = db.Column(db.Float)
    max_price = db.Column(db.Float)
    modal_price = db.Column(db.Float, index=True)
    arrival_date = db.Column(db.DateTime, index=True)
    recorded_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Indexes
    __table_args__ = (
        db.Index('idx_price_district_crop', 'district', 'crop'),
        db.Index('idx_price_crop_date', 'crop', 'arrival_date'),
        db.Index('idx_price_mandi', 'mandi'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'district': self.district,
            'mandi': self.mandi,
            'crop': self.crop,
            'variety': self.variety,
            'grade': self.grade,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'modal_price': self.modal_price,
            'arrival_date': self.arrival_date.isoformat() if self.arrival_date else None,
            'recorded_date': self.recorded_date.isoformat() if self.recorded_date else None
        }

    def __repr__(self):
        return f'<PriceData {self.crop} - {self.district} - {self.modal_price}>'