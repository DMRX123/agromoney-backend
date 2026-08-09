"""
Notification routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import json
from app import db
from app.models import Notification, User

notification_bp = Blueprint('notifications', __name__)


@notification_bp.route('', methods=['GET'])
def get_notifications():
    """Get notifications with filters"""
    try:
        user_id = request.args.get('user_id', type=int)
        district = request.args.get('district')
        crop = request.args.get('crop')
        notification_type = request.args.get('type')
        language = request.args.get('language', 'english')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))

        query = Notification.query

        if user_id:
            query = query.filter(
                (Notification.user_id == user_id) |
                (Notification.user_id.is_(None))
            )

            # Get user preferences
            user = User.query.get(user_id)
            if user:
                if user.district:
                    query = query.filter(
                        (Notification.target_district == user.district) |
                        (Notification.target_district.is_(None))
                    )

                user_crops = []
                if user.crops_grown:
                    try:
                        user_crops = json.loads(user.crops_grown)
                    except:
                        pass

                if user_crops:
                    from sqlalchemy import or_
                    query = query.filter(
                        or_(
                            Notification.target_crop.in_(user_crops),
                            Notification.target_crop.is_(None)
                        )
                    )

        if district:
            query = query.filter(
                (Notification.target_district == district) |
                (Notification.target_district.is_(None))
            )
        if crop:
            query = query.filter(
                (Notification.target_crop == crop) |
                (Notification.target_crop.is_(None))
            )
        if notification_type:
            query = query.filter_by(notification_type=notification_type)

        total = query.count()
        notifications = query.order_by(
            Notification.created_at.desc()
        ).paginate(page=page, per_page=limit)

        return jsonify({
            'success': True,
            'data': [n.to_dict(language) for n in notifications.items],
            'total': total,
            'page': page,
            'limit': limit,
            'pages': notifications.pages
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching notifications: {str(e)}'
        }), 500


@notification_bp.route('', methods=['POST'])
@jwt_required()
def create_notification():
    """Create a new notification"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user or not user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403

        data = request.json

        required = ['title', 'message']
        for field in required:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'{field} is required'
                }), 400

        notification = Notification(
            title=data['title'],
            title_hindi=data.get('title_hindi'),
            message=data['message'],
            message_hindi=data.get('message_hindi'),
            notification_type=data.get('notification_type', 'general'),
            target_district=data.get('target_district'),
            target_crop=data.get('target_crop'),
            target_role=data.get('target_role', 'all')
        )

        db.session.add(notification)
        db.session.commit()

        # Send notification (async in production)
        from app.services import NotificationService
        NotificationService.send_notification(notification)

        return jsonify({
            'success': True,
            'message': 'Notification created and sent',
            'notification_id': notification.id,
            'notification': notification.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating notification: {str(e)}'
        }), 500


@notification_bp.route('/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
    """Get specific notification"""
    try:
        language = request.args.get('language', 'english')
        notification = Notification.query.get_or_404(notification_id)

        return jsonify({
            'success': True,
            'notification': notification.to_dict(language)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching notification: {str(e)}'
        }), 500


@notification_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    """Delete a notification"""
    try:
        user_id = int(get_jwt_identity())
        notification = Notification.query.get_or_404(notification_id)
        
        # Check if user owns this notification or is admin
        if notification.user_id and notification.user_id != user_id:
            user = User.query.get(user_id)
            if not user or not user.is_admin:
                return jsonify({
                    'success': False,
                    'message': 'You can only delete your own notifications'
                }), 403
        
        db.session.delete(notification)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Notification deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting notification: {str(e)}'
        }), 500


@notification_bp.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(notification_id):
    """Mark notification as read"""
    try:
        user_id = int(get_jwt_identity())
        notification = Notification.query.get_or_404(notification_id)

        if notification.user_id and notification.user_id != user_id:
            return jsonify({
                'success': False,
                'message': 'You can only mark your own notifications as read'
            }), 403

        notification.mark_as_read()
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Notification marked as read'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error marking notification as read: {str(e)}'
        }), 500


@notification_bp.route('/price-alert', methods=['POST'])
@jwt_required()
def create_price_alert():
    """Create a price alert notification"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        data = request.json
        required = ['crop', 'district', 'price_change', 'current_price']

        for field in required:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'{field} is required'
                }), 400

        crop = data['crop']
        district = data['district']
        price_change = float(data['price_change'])
        current_price = float(data['current_price'])

        direction = "increased" if price_change > 0 else "decreased"

        title = f"{crop} Price Alert - {district}"
        message = f"{crop} prices have {direction} by {abs(price_change):.1f}% in {district}. Current price: ₹{current_price:.2f}/quintal."

        title_hindi = f"{crop} कीमत चेतावनी - {district}"
        message_hindi = f"{district} में {crop} की कीमतें {abs(price_change):.1f}% {direction} हैं। वर्तमान कीमत: ₹{current_price:.2f}/क्विंटल।"

        notification = Notification(
            title=title,
            message=message,
            title_hindi=title_hindi,
            message_hindi=message_hindi,
            notification_type='price_alert',
            target_district=district,
            target_crop=crop
        )

        db.session.add(notification)
        db.session.commit()

        from app.services import NotificationService
        NotificationService.send_notification(notification)

        return jsonify({
            'success': True,
            'message': 'Price alert created',
            'notification_id': notification.id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating price alert: {str(e)}'
        }), 500