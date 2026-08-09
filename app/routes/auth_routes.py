"""
Authentication routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies
)
from datetime import datetime
import json
import re
from app import db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserUpdate

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.json
        schema = UserCreate(**data)

        # Check if user exists
        if User.query.filter_by(phone=schema.phone).first():
            return jsonify({
                'success': False,
                'message': 'Phone number already registered'
            }), 400

        if schema.email and User.query.filter_by(email=schema.email).first():
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 400

        # Create user
        user = User(
            name=schema.name,
            phone=schema.phone,
            email=schema.email,
            district=schema.district,
            village=schema.village,
            land_area=schema.land_area,
            soil_type=schema.soil_type,
            language=schema.language,
            crops_grown=json.dumps(schema.crops_grown)
        )

        # In production: hash password
        if hasattr(schema, 'password') and schema.password:
            user.password_hash = schema.password  # TODO: Use bcrypt

        db.session.add(user)
        db.session.commit()

        # Generate tokens
        tokens = user.generate_tokens()

        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'tokens': tokens
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user with phone and password/OTP"""
    try:
        data = request.json
        schema = UserLogin(**data)

        user = User.query.filter_by(phone=schema.phone).first()

        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404

        # OTP login (simplified - in production verify OTP)
        if schema.otp:
            # In production: Verify OTP from cache/SMS service
            if schema.otp == '123456':  # Demo OTP
                user.update_last_login()
                tokens = user.generate_tokens()
                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'user': user.to_dict(),
                    'tokens': tokens
                })

        # Password login
        if schema.password:
            # In production: Verify hashed password
            if user.password_hash == schema.password:
                user.update_last_login()
                tokens = user.generate_tokens()
                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'user': user.to_dict(),
                    'tokens': tokens
                })

        return jsonify({
            'success': False,
            'message': 'Invalid credentials'
        }), 401

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login failed: {str(e)}'
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user"""
    response = jsonify({
        'success': True,
        'message': 'Logout successful'
    })
    unset_jwt_cookies(response)
    return response


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404

        return jsonify({
            'success': True,
            'user': user.to_dict()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching profile: {str(e)}'
        }), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404

        data = request.json
        schema = UserUpdate(**data)

        if schema.name is not None:
            user.name = schema.name
        if schema.district is not None:
            user.district = schema.district
        if schema.village is not None:
            user.village = schema.village
        if schema.land_area is not None:
            user.land_area = schema.land_area
        if schema.soil_type is not None:
            user.soil_type = schema.soil_type
        if schema.language is not None:
            user.language = schema.language
        if schema.crops_grown is not None:
            user.crops_grown = json.dumps(schema.crops_grown)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating profile: {str(e)}'
        }), 500


@auth_bp.route('/send-otp', methods=['POST'])
def send_otp():
    """Send OTP to user's phone"""
    try:
        data = request.json
        phone = data.get('phone')

        if not phone:
            return jsonify({
                'success': False,
                'message': 'Phone number is required'
            }), 400

        # Validate phone number
        if not re.match(r'^[6-9]\d{9}$', phone):
            return jsonify({
                'success': False,
                'message': 'Invalid phone number format'
            }), 400

        # In production: Send actual OTP via SMS service
        # For demo, return a fixed OTP with expiry
        otp = '123456'
        expires_in = 300  # 5 minutes

        return jsonify({
            'success': True,
            'message': 'OTP sent successfully',
            'otp': otp,  # In production, don't return OTP in response
            'expires_in': expires_in,
            'phone': phone
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error sending OTP: {str(e)}'
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """Refresh access token"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404

        new_access_token = create_access_token(identity=str(user_id))

        return jsonify({
            'success': True,
            'access_token': new_access_token
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error refreshing token: {str(e)}'
        }), 500