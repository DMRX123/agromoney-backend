"""
Notification model
"""
from datetime import datetime
from app import db


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    title_hindi = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    message_hindi = db.Column(db.Text)
    notification_type = db.Column(db.String(50), index=True)
    target_district = db.Column(db.String(100), index=True)
    target_crop = db.Column(db.String(100), index=True)
    target_role = db.Column(db.String(20), default='all')
    is_read = db.Column(db.Boolean, default=False)
    is_sent = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship - ✅ FIX: Add foreign_keys
    user = db.relationship('User', foreign_keys=[user_id], back_populates='notifications')

    def to_dict(self, language='english'):
        base = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title if language == 'english' else (self.title_hindi or self.title),
            'message': self.message if language == 'english' else (self.message_hindi or self.message),
            'type': self.notification_type,
            'target_district': self.target_district,
            'target_crop': self.target_crop,
            'is_read': self.is_read,
            'is_sent': self.is_sent,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'created_at': self.created_at.isoformat()
        }
        return base

    def mark_as_sent(self):
        self.is_sent = True
        self.sent_at = datetime.utcnow()

    def mark_as_read(self):
        self.is_read = True

    def __repr__(self):
        return f'<Notification {self.title}>'