"""
Admin routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app import db
from app.models import User, PriceData, MarketProduct, Notification
from app.services import AgmarknetService

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    """Get admin dashboard statistics"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user or not user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403

        # User stats
        total_users = User.query.count()
        users_today = User.query.filter(
            User.created_at >= datetime.now().date()
        ).count()

        # Price stats
        total_prices = PriceData.query.count()
        latest_price = PriceData.query.order_by(
            PriceData.arrival_date.desc()
        ).first()

        # Marketplace stats
        total_listings = MarketProduct.query.count()
        active_listings = MarketProduct.query.filter_by(status='available').count()
        verified_listings = MarketProduct.query.filter_by(is_verified=True).count()

        # Notification stats
        total_notifications = Notification.query.count()
        sent_notifications = Notification.query.filter_by(is_sent=True).count()

        # Recent activity
        recent_users = User.query.order_by(
            User.created_at.desc()
        ).limit(5).all()

        recent_listings = MarketProduct.query.order_by(
            MarketProduct.created_at.desc()
        ).limit(5).all()

        return jsonify({
            'success': True,
            'stats': {
                'users': {
                    'total': total_users,
                    'today': users_today,
                    'recent': [u.to_dict() for u in recent_users]
                },
                'prices': {
                    'total': total_prices,
                    'latest_update': latest_price.arrival_date.isoformat() if latest_price else None
                },
                'marketplace': {
                    'total': total_listings,
                    'active': active_listings,
                    'verified': verified_listings,
                    'verification_rate': round((verified_listings / active_listings * 100), 1) if active_listings > 0 else 0,
                    'recent': [l.to_dict() for l in recent_listings]
                },
                'notifications': {
                    'total': total_notifications,
                    'sent': sent_notifications,
                    'delivery_rate': round((sent_notifications / total_notifications * 100), 1) if total_notifications > 0 else 0
                }
            },
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching dashboard: {str(e)}'
        }), 500


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users (admin only)"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user or not user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403

        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        search = request.args.get('search')
        district = request.args.get('district')

        query = User.query

        if search:
            query = query.filter(
                (User.name.ilike(f'%{search}%')) |
                (User.phone.ilike(f'%{search}%'))
            )
        if district:
            query = query.filter_by(district=district)

        total = query.count()
        users = query.order_by(
            User.created_at.desc()
        ).paginate(page=page, per_page=limit)

        return jsonify({
            'success': True,
            'data': [u.to_dict() for u in users.items],
            'total': total,
            'page': page,
            'limit': limit,
            'pages': users.pages
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching users: {str(e)}'
        }), 500


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user (admin only)"""
    try:
        admin_id = int(get_jwt_identity())
        admin = User.query.get(admin_id)

        if not admin or not admin.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403

        user = User.query.get_or_404(user_id)
        data = request.json

        updatable = ['name', 'district', 'village', 'land_area', 'soil_type', 'language', 'is_active', 'is_admin']
        for field in updatable:
            if field in data:
                setattr(user, field, data[field])

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'User updated successfully',
            'user': user.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating user: {str(e)}'
        }), 500


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete user (admin only)"""
    try:
        admin_id = int(get_jwt_identity())
        admin = User.query.get(admin_id)

        if not admin or not admin.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403

        user = User.query.get_or_404(user_id)

        if user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Cannot delete admin user'
            }), 400

        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting user: {str(e)}'
        }), 500


@admin_bp.route('/sync', methods=['POST'])
@jwt_required()
def sync_data():
    """Force sync data from AGMARKNET"""
    try:
        admin_id = int(get_jwt_identity())
        admin = User.query.get(admin_id)

        if not admin or not admin.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403

        service = AgmarknetService()
        result = service.fetch_and_save_prices()

        return jsonify({
            'success': True,
            'message': f'Synced {result.get("count", 0)} price records',
            'details': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error syncing data: {str(e)}'
        }), 500


@admin_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    """Get system analytics"""
    try:
        admin_id = int(get_jwt_identity())
        admin = User.query.get(admin_id)

        if not admin or not admin.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403

        # User growth by month
        user_growth = db.session.query(
            func.strftime('%Y-%m', User.created_at).label('month'),
            func.count(User.id).label('count')
        ).group_by('month').order_by('month').all()

        # Crop distribution in marketplace
        crop_dist = db.session.query(
            MarketProduct.crop,
            func.count(MarketProduct.id)
        ).filter_by(status='available')\
         .group_by(MarketProduct.crop)\
         .order_by(func.count(MarketProduct.id).desc())\
         .limit(10).all()

        # District-wise price data
        district_prices = db.session.query(
            PriceData.district,
            func.avg(PriceData.modal_price).label('avg_price'),
            func.count(PriceData.id).label('count')
        ).filter(PriceData.modal_price.isnot(None))\
         .group_by(PriceData.district)\
         .order_by(func.count(PriceData.id).desc())\
         .limit(10).all()

        # Notification engagement
        notif_stats = db.session.query(
            Notification.notification_type,
            func.count(Notification.id).label('total'),
            func.sum(Notification.is_sent).label('sent')
        ).group_by(Notification.notification_type).all()

        return jsonify({
            'success': True,
            'analytics': {
                'user_growth': [{'month': m, 'count': c} for m, c in user_growth],
                'crop_distribution': [{'crop': c, 'count': cnt} for c, cnt in crop_dist],
                'district_prices': [{'district': d, 'avg_price': round(avg, 2) if avg else 0, 'count': cnt}
                                   for d, avg, cnt in district_prices],
                'notification_stats': [{'type': t, 'total': tot, 'sent': sent or 0}
                                     for t, tot, sent in notif_stats]
            },
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching analytics: {str(e)}'
        }), 500