from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import random
from models.market_models import BuyingRequest
from models.market_models import User, SellingListing, PriceAlert, MarketTransaction, UserPreference, MarketInsight

user_bp = Blueprint('user', __name__)

# In-memory storage for demo (replace with database in production)
users = []
listings = []
price_alerts = []
notifications = []
buying_requests = []
transactions = []
user_preferences = []
market_insights = []

class Notification:
    def __init__(self, id, user_id, title, message, type='info', related_id=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.message = message
        self.type = type  # info, alert, price_alert, system
        self.related_id = related_id
        self.created_at = datetime.now()
        self.is_read = False

@user_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('name') or not data.get('phone') or not data.get('district'):
            return jsonify({
                'success': False,
                'error': 'Name, phone, and district are required fields'
            }), 400
        
        # Check if user already exists
        existing_user = next((u for u in users if u.phone == data.get('phone')), None)
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'User with this phone number already exists'
            }), 409
        
        user_id = len(users) + 1
        user = User(
            id=user_id,
            name=data.get('name'),
            phone=data.get('phone'),
            district=data.get('district'),
            language=data.get('language', 'en'),
            user_type=data.get('user_type', 'farmer'),
            email=data.get('email'),
            preferred_crops=data.get('preferred_crops', []),
            experience_years=data.get('experience_years', 0),
            farm_size=data.get('farm_size'),
            verification_status=data.get('verification_status', 'pending')
        )
        
        users.append(user)
        
        # Create default preferences
        preferences = UserPreference(
            user_id=user_id,
            preferred_districts=[data.get('district')],
            preferred_crops=data.get('preferred_crops', []),
            market_analysis_period='10_years'
        )
        user_preferences.append(preferences)
        
        # Create welcome notification
        welcome_notification = Notification(
            id=len(notifications) + 1,
            user_id=user_id,
            title=f"Welcome to AgroMoney, {user.name}!",
            message="Thank you for registering. Start by creating your first listing or setting up price alerts.",
            type='info'
        )
        notifications.append(welcome_notification)
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user_id': user.id,
            'user': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Registration failed: {str(e)}'
        }), 500

@user_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    try:
        user = next((u for u in users if u.id == user_id), None)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Get user preferences
        preferences = next((p for p in user_preferences if p.user_id == user_id), None)
        
        # Get user stats
        user_listings = [l for l in listings if l.user_id == user_id]
        user_alerts = [a for a in price_alerts if a.user_id == user_id]
        user_transactions = [t for t in transactions if t.buyer_id == user_id or t.seller_id == user_id]
        
        return jsonify({
            'success': True,
            'profile': user.to_dict(),
            'preferences': preferences.to_dict() if preferences else None,
            'stats': {
                'total_listings': len(user_listings),
                'active_listings': len([l for l in user_listings if l.status == 'active']),
                'price_alerts': len(user_alerts),
                'active_alerts': len([a for a in user_alerts if a.is_active]),
                'total_transactions': len(user_transactions),
                'reliability_score': user._calculate_reliability_score()
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch profile: {str(e)}'
        }), 500

@user_bp.route('/profile/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    try:
        data = request.get_json()
        user = next((u for u in users if u.id == user_id), None)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Update fields if provided
        if 'name' in data:
            user.name = data['name']
        if 'district' in data:
            user.district = data['district']
        if 'language' in data:
            user.language = data['language']
        if 'email' in data:
            user.email = data['email']
        if 'preferred_crops' in data:
            user.preferred_crops = data['preferred_crops']
        if 'experience_years' in data:
            user.experience_years = data['experience_years']
        if 'farm_size' in data:
            user.farm_size = data['farm_size']
        
        user.updated_at = datetime.now()
        
        # Update preferences if provided
        if 'preferences' in data:
            preferences = next((p for p in user_preferences if p.user_id == user_id), None)
            if preferences:
                pref_data = data['preferences']
                if 'preferred_districts' in pref_data:
                    preferences.preferred_districts = pref_data['preferred_districts']
                if 'preferred_crops' in pref_data:
                    preferences.preferred_crops = pref_data['preferred_crops']
                if 'price_update_frequency' in pref_data:
                    preferences.price_update_frequency = pref_data['price_update_frequency']
                if 'market_analysis_period' in pref_data:
                    preferences.market_analysis_period = pref_data['market_analysis_period']
                preferences.updated_at = datetime.now()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update profile: {str(e)}'
        }), 500

@user_bp.route('/listings', methods=['POST'])
def create_listing():
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['user_id', 'crop', 'district', 'market', 'quantity', 'quality', 'contact_info']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Verify user exists
        user = next((u for u in users if u.id == data.get('user_id')), None)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        listing_id = len(listings) + 1
        listing = SellingListing(
            id=listing_id,
            user_id=data.get('user_id'),
            crop=data.get('crop'),
            district=data.get('district'),
            market=data.get('market'),
            quantity=data.get('quantity'),
            quality=data.get('quality'),
            contact_info=data.get('contact_info'),
            expected_price=data.get('price'),
            description=data.get('description', ''),
            harvest_date=data.get('harvest_date'),
            storage_type=data.get('storage_type', 'conventional'),
            organic_certified=data.get('organic_certified', False),
            moisture_content=data.get('moisture_content')
        )
        
        listings.append(listing)
        
        # Create notification
        listing_notification = Notification(
            id=len(notifications) + 1,
            user_id=user.id,
            title="Listing Created Successfully",
            message=f"Your {data.get('crop')} listing has been created and is now visible to buyers.",
            type='info',
            related_id=listing.id
        )
        notifications.append(listing_notification)
        
        return jsonify({
            'success': True,
            'message': 'Listing created successfully',
            'listing': listing.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create listing: {str(e)}'
        }), 500

@user_bp.route('/listings', methods=['GET'])
def get_listings():
    try:
        crop = request.args.get('crop')
        district = request.args.get('district')
        user_id = request.args.get('user_id', type=int)
        status = request.args.get('status', 'active')
        
        filtered_listings = listings
        
        # Filter by user if user_id provided
        if user_id:
            filtered_listings = [l for l in filtered_listings if l.user_id == user_id]
        
        # Filter by status
        filtered_listings = [l for l in filtered_listings if l.status == status]
        
        # Additional filters
        if crop:
            filtered_listings = [l for l in filtered_listings if l.crop.lower() == crop.lower()]
        if district:
            filtered_listings = [l for l in filtered_listings if l.district.lower() == district.lower()]
        
        # Sort by creation date (newest first)
        filtered_listings.sort(key=lambda x: x.created_at, reverse=True)
        
        return jsonify({
            'success': True,
            'listings': [listing.to_dict() for listing in filtered_listings],
            'count': len(filtered_listings)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch listings: {str(e)}'
        }), 500

@user_bp.route('/listings/<int:listing_id>', methods=['PUT'])
def update_listing(listing_id):
    try:
        data = request.get_json()
        listing = next((l for l in listings if l.id == listing_id), None)
        
        if not listing:
            return jsonify({
                'success': False,
                'error': 'Listing not found'
            }), 404
        
        # Update fields if provided
        updatable_fields = ['quantity', 'quality', 'expected_price', 'description', 'contact_info', 'status']
        for field in updatable_fields:
            if field in data:
                setattr(listing, field, data[field])
        
        listing.updated_at = datetime.now()
        
        return jsonify({
            'success': True,
            'message': 'Listing updated successfully',
            'listing': listing.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update listing: {str(e)}'
        }), 500

@user_bp.route('/listings/<int:listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    try:
        listing = next((l for l in listings if l.id == listing_id), None)
        
        if not listing:
            return jsonify({
                'success': False,
                'error': 'Listing not found'
            }), 404
        
        # Soft delete by changing status
        listing.status = 'expired'
        listing.updated_at = datetime.now()
        
        return jsonify({
            'success': True,
            'message': 'Listing deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to delete listing: {str(e)}'
        }), 500

@user_bp.route('/alerts', methods=['POST'])
def create_price_alert():
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['user_id', 'crop', 'target_price']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Verify user exists
        user = next((u for u in users if u.id == data.get('user_id')), None)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        alert_id = len(price_alerts) + 1
        alert = PriceAlert(
            id=alert_id,
            user_id=data.get('user_id'),
            crop=data.get('crop'),
            target_price=data.get('target_price'),
            condition=data.get('condition', 'above'),
            district=data.get('district', user.district),
            alert_type=data.get('alert_type', 'price'),
            notification_method=data.get('notification_method', 'sms'),
            timeframe=data.get('timeframe', 'any'),
            data_source=data.get('data_source', '10_year_analysis')
        )
        
        price_alerts.append(alert)
        
        # Create notification
        alert_notification = Notification(
            id=len(notifications) + 1,
            user_id=user.id,
            title="Price Alert Created",
            message=f"Price alert for {data.get('crop')} set at ₹{data.get('target_price')} per quintal.",
            type='alert',
            related_id=alert.id
        )
        notifications.append(alert_notification)
        
        return jsonify({
            'success': True,
            'message': 'Price alert created successfully',
            'alert': alert.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create price alert: {str(e)}'
        }), 500

@user_bp.route('/alerts', methods=['GET'])
def get_price_alerts():
    try:
        user_id = request.args.get('user_id', type=int)
        crop = request.args.get('crop')
        is_active = request.args.get('is_active', type=bool)
        
        filtered_alerts = price_alerts
        
        if user_id:
            filtered_alerts = [a for a in filtered_alerts if a.user_id == user_id]
        if crop:
            filtered_alerts = [a for a in filtered_alerts if a.crop.lower() == crop.lower()]
        if is_active is not None:
            filtered_alerts = [a for a in filtered_alerts if a.is_active == is_active]
        
        # Sort by creation date (newest first)
        filtered_alerts.sort(key=lambda x: x.created_at, reverse=True)
        
        return jsonify({
            'success': True,
            'alerts': [alert.to_dict() for alert in filtered_alerts],
            'count': len(filtered_alerts)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch price alerts: {str(e)}'
        }), 500

@user_bp.route('/alerts/<int:alert_id>', methods=['PUT'])
def update_price_alert(alert_id):
    try:
        data = request.get_json()
        alert = next((a for a in price_alerts if a.id == alert_id), None)
        
        if not alert:
            return jsonify({
                'success': False,
                'error': 'Price alert not found'
            }), 404
        
        # Update fields if provided
        if 'target_price' in data:
            alert.target_price = data['target_price']
        if 'condition' in data:
            alert.condition = data['condition']
        if 'is_active' in data:
            alert.is_active = data['is_active']
        if 'district' in data:
            alert.district = data['district']
        if 'notification_method' in data:
            alert.notification_method = data['notification_method']
        
        alert.last_checked = datetime.now()
        
        return jsonify({
            'success': True,
            'message': 'Price alert updated successfully',
            'alert': alert.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update price alert: {str(e)}'
        }), 500

@user_bp.route('/alerts/<int:alert_id>', methods=['DELETE'])
def delete_price_alert(alert_id):
    try:
        alert = next((a for a in price_alerts if a.id == alert_id), None)
        
        if not alert:
            return jsonify({
                'success': False,
                'error': 'Price alert not found'
            }), 404
        
        # Soft delete by deactivating
        alert.is_active = False
        
        return jsonify({
            'success': True,
            'message': 'Price alert deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to delete price alert: {str(e)}'
        }), 500

@user_bp.route('/notifications', methods=['GET'])
def get_notifications():
    try:
        user_id = request.args.get('user_id', type=int)
        unread_only = request.args.get('unread_only', type=bool)
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'User ID is required'
            }), 400
        
        user_notifications = [n for n in notifications if n.user_id == user_id]
        
        if unread_only:
            user_notifications = [n for n in user_notifications if not n.is_read]
        
        # Sort by creation date (newest first)
        user_notifications.sort(key=lambda x: x.created_at, reverse=True)
        
        return jsonify({
            'success': True,
            'notifications': [{
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'type': n.type,
                'related_id': n.related_id,
                'is_read': n.is_read,
                'created_at': n.created_at.isoformat()
            } for n in user_notifications],
            'count': len(user_notifications),
            'unread_count': len([n for n in user_notifications if not n.is_read])
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch notifications: {str(e)}'
        }), 500

@user_bp.route('/notifications/<int:notification_id>/read', methods=['PUT'])
def mark_notification_read(notification_id):
    try:
        notification = next((n for n in notifications if n.id == notification_id), None)
        
        if not notification:
            return jsonify({
                'success': False,
                'error': 'Notification not found'
            }), 404
        
        notification.is_read = True
        
        return jsonify({
            'success': True,
            'message': 'Notification marked as read'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to mark notification as read: {str(e)}'
        }), 500

@user_bp.route('/notifications/read-all', methods=['PUT'])
def mark_all_notifications_read():
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'User ID is required'
            }), 400
        
        user_notifications = [n for n in notifications if n.user_id == user_id and not n.is_read]
        
        for notification in user_notifications:
            notification.is_read = True
        
        return jsonify({
            'success': True,
            'message': f'Marked {len(user_notifications)} notifications as read'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to mark notifications as read: {str(e)}'
        }), 500

# Background task simulation (would run as a separate process in production)
@user_bp.route('/simulate/check-alerts', methods=['POST'])
def simulate_check_alerts():
    """Simulate checking price alerts against current market prices"""
    try:
        # Get current market prices (in real app, this would come from market API)
        current_prices = {
            "Wheat": 2450,
            "Rice": 3100,
            "Maize": 2250,
            "Soybean": 4850,
            "Gram": 5250,
            "Tomato": 1600,
            "Onion": 2100,
            "Potato": 1850
        }
        
        triggered_alerts = []
        
        for alert in price_alerts:
            if not alert.is_active or alert.triggered:
                continue
            
            current_price = current_prices.get(alert.crop, 3000)
            
            if alert.trigger_alert(current_price):
                # Create notification for triggered alert
                notification = Notification(
                    id=len(notifications) + 1,
                    user_id=alert.user_id,
                    title="Price Alert Triggered!",
                    message=f"{alert.crop} price is now ₹{current_price} (your target: ₹{alert.target_price})",
                    type='price_alert',
                    related_id=alert.id
                )
                notifications.append(notification)
                
                triggered_alerts.append({
                    'alert_id': alert.id,
                    'crop': alert.crop,
                    'target_price': alert.target_price,
                    'current_price': current_price,
                    'condition': alert.condition
                })
        
        return jsonify({
            'success': True,
            'message': f'Checked {len(price_alerts)} alerts, triggered {len(triggered_alerts)}',
            'triggered_alerts': triggered_alerts
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to check alerts: {str(e)}'
        }), 500

@user_bp.route('/buying-requests', methods=['POST'])
def create_buying_request():
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['user_id', 'crop', 'district', 'quantity', 'contact_info']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Verify user exists
        user = next((u for u in users if u.id == data.get('user_id')), None)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        request_id = len(buying_requests) + 1
        buying_request = BuyingRequest(
            id=request_id,
            user_id=data.get('user_id'),
            crop=data.get('crop'),
            district=data.get('district'),
            quantity=data.get('quantity'),
            contact_info=data.get('contact_info'),
            max_price=data.get('max_price'),
            quality_requirements=data.get('quality_requirements'),
            delivery_required=data.get('delivery_required', False),
            urgency=data.get('urgency', 'normal'),
            payment_terms=data.get('payment_terms', 'immediate'),
            preferred_harvest_date=data.get('preferred_harvest_date')
        )
        
        buying_requests.append(buying_request)
        
        return jsonify({
            'success': True,
            'message': 'Buying request created successfully',
            'buying_request': buying_request.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create buying request: {str(e)}'
        }), 500

@user_bp.route('/buying-requests', methods=['GET'])
def get_buying_requests():
    try:
        user_id = request.args.get('user_id', type=int)
        crop = request.args.get('crop')
        district = request.args.get('district')
        status = request.args.get('status', 'active')
        
        filtered_requests = buying_requests
        
        if user_id:
            filtered_requests = [r for r in filtered_requests if r.user_id == user_id]
        
        if crop:
            filtered_requests = [r for r in filtered_requests if r.crop.lower() == crop.lower()]
        
        if district:
            filtered_requests = [r for r in filtered_requests if r.district.lower() == district.lower()]
        
        if status:
            filtered_requests = [r for r in filtered_requests if r.status == status]
        
        filtered_requests.sort(key=lambda x: x.created_at, reverse=True)
        
        return jsonify({
            'success': True,
            'buying_requests': [req.to_dict() for req in filtered_requests],
            'count': len(filtered_requests)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch buying requests: {str(e)}'
        }), 500