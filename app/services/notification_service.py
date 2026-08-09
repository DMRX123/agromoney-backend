"""
Notification Service
"""
import logging
from datetime import datetime
from app import db
from app.models import Notification, User

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for handling notifications"""

    @staticmethod
    def send_notification(notification: Notification) -> int:
        """Send notification to users"""
        try:
            # Get target users
            users = NotificationService._get_target_users(notification)

            # In production: Send push notifications via FCM/APNS
            # For demo: Just mark as sent
            notification.is_sent = True
            notification.sent_at = datetime.utcnow()
            db.session.commit()

            logger.info(f"Notification '{notification.title}' sent to {len(users)} users")
            return len(users)

        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            return 0

    @staticmethod
    def _get_target_users(notification: Notification):
        """Get target users for notification"""
        query = User.query.filter_by(is_active=True)

        if notification.target_role == 'admin':
            query = query.filter_by(is_admin=True)
        elif notification.target_role == 'farmer':
            query = query.filter_by(is_admin=False)

        if notification.target_district:
            query = query.filter_by(district=notification.target_district)

        return query.all()

    @staticmethod
    def create_price_alert(
        crop: str,
        district: str,
        price_change: float,
        current_price: float
    ) -> Notification:
        """Create price alert notification"""
        direction = "increased" if price_change > 0 else "decreased"

        title = f"{crop} Price Alert - {district}"
        message = f"{crop} prices have {direction} by {abs(price_change):.1f}% in {district}. Current price: ₹{current_price:.2f}/quintal."

        notification = Notification(
            title=title,
            message=message,
            notification_type='price_alert',
            target_district=district,
            target_crop=crop
        )

        db.session.add(notification)
        db.session.commit()

        return notification