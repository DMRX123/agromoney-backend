"""
Marketplace routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, func
from datetime import datetime
from app import db
from app.models import MarketProduct, User, PriceData

market_bp = Blueprint('market', __name__)


@market_bp.route('', methods=['GET'])
def get_listings():
    """Get marketplace listings with filters"""
    try:
        crop = request.args.get('crop')
        district = request.args.get('district')
        mandi = request.args.get('mandi')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        status = request.args.get('status', 'available')
        language = request.args.get('language', 'english')
        verified_only = request.args.get('verified', 'false').lower() == 'true'
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))

        query = MarketProduct.query.filter_by(status=status)

        if crop:
            query = query.filter(MarketProduct.crop == crop)
        if district:
            query = query.filter(MarketProduct.district == district)
        if mandi:
            query = query.filter(MarketProduct.mandi == mandi)
        if min_price:
            query = query.filter(MarketProduct.price_per_unit >= float(min_price))
        if max_price:
            query = query.filter(MarketProduct.price_per_unit <= float(max_price))
        if verified_only:
            query = query.filter_by(is_verified=True)

        total = query.count()
        listings = query.order_by(
            MarketProduct.is_verified.desc(),
            MarketProduct.created_at.desc()
        ).paginate(page=page, per_page=limit)

        return jsonify({
            'success': True,
            'data': [l.to_dict(language) for l in listings.items],
            'total': total,
            'page': page,
            'limit': limit,
            'pages': listings.pages
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching listings: {str(e)}'
        }), 500


@market_bp.route('', methods=['POST'])
@jwt_required()
def create_listing():
    """Create a new marketplace listing"""
    try:
        user_id = int(get_jwt_identity())
        data = request.json

        # Validate
        required = ['crop', 'quantity', 'contact_number']
        for field in required:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'{field} is required'
                }), 400

        listing = MarketProduct(
            user_id=user_id,
            crop=data['crop'],
            variety=data.get('variety'),
            quantity=float(data['quantity']),
            unit=data.get('unit', 'quintal'),
            price_per_unit=float(data['price_per_unit']) if data.get('price_per_unit') else None,
            district=data.get('district'),
            mandi=data.get('mandi'),
            village=data.get('village'),
            description=data.get('description'),
            description_hindi=data.get('description_hindi'),
            contact_number=data['contact_number'],
            image_url=data.get('image_url')
        )

        db.session.add(listing)
        db.session.commit()

        # Auto-verify based on market price
        if listing.price_per_unit and listing.district and listing.crop:
            latest_price = PriceData.query.filter_by(
                district=listing.district,
                crop=listing.crop
            ).order_by(PriceData.arrival_date.desc()).first()

            if latest_price and latest_price.modal_price:
                market_price = latest_price.modal_price
                user_price = listing.price_per_unit
                if abs(user_price - market_price) / market_price <= 0.2:
                    listing.verify(admin_id=1)  # Auto-verify
                    db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Product listed successfully',
            'listing_id': listing.id,
            'listing': listing.to_dict(),
            'auto_verified': listing.is_verified
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating listing: {str(e)}'
        }), 500


@market_bp.route('/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
    """Get specific listing"""
    try:
        language = request.args.get('language', 'english')
        listing = MarketProduct.query.get_or_404(listing_id)

        return jsonify({
            'success': True,
            'listing': listing.to_dict(language)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching listing: {str(e)}'
        }), 500


@market_bp.route('/<int:listing_id>', methods=['PUT'])
@jwt_required()
def update_listing(listing_id):
    """Update listing"""
    try:
        user_id = int(get_jwt_identity())
        listing = MarketProduct.query.get_or_404(listing_id)

        if listing.user_id != user_id:
            return jsonify({
                'success': False,
                'message': 'You can only update your own listings'
            }), 403

        data = request.json
        updatable = ['quantity', 'price_per_unit', 'description',
                     'description_hindi', 'contact_number', 'image_url']

        for field in updatable:
            if field in data:
                setattr(listing, field, data[field])

        listing.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Listing updated successfully',
            'listing': listing.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating listing: {str(e)}'
        }), 500


@market_bp.route('/<int:listing_id>/status', methods=['PUT'])
@jwt_required()
def update_status(listing_id):
    """Update listing status"""
    try:
        user_id = int(get_jwt_identity())
        listing = MarketProduct.query.get_or_404(listing_id)

        if listing.user_id != user_id:
            return jsonify({
                'success': False,
                'message': 'You can only update your own listings'
            }), 403

        data = request.json
        new_status = data.get('status')

        valid = ['available', 'sold', 'reserved', 'removed']
        if new_status not in valid:
            return jsonify({
                'success': False,
                'message': f'Invalid status. Must be: {", ".join(valid)}'
            }), 400

        listing.update_status(new_status)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Status updated to {new_status}',
            'listing': listing.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating status: {str(e)}'
        }), 500


@market_bp.route('/<int:listing_id>/verify', methods=['POST'])
@jwt_required()
def verify_listing(listing_id):
    """Verify a listing (admin only)"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user or not user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403

        listing = MarketProduct.query.get_or_404(listing_id)
        listing.verify(user_id)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Listing verified successfully',
            'listing': listing.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error verifying listing: {str(e)}'
        }), 500


@market_bp.route('/search', methods=['GET'])
def search_listings():
    """Search marketplace listings"""
    try:
        query = request.args.get('q', '')
        language = request.args.get('language', 'english')
        limit = int(request.args.get('limit', 20))

        if len(query) < 2:
            return jsonify({
                'success': False,
                'message': 'Search query must be at least 2 characters'
            }), 400

        listings = MarketProduct.query.filter(
            MarketProduct.status == 'available',
            or_(
                MarketProduct.crop.ilike(f'%{query}%'),
                MarketProduct.variety.ilike(f'%{query}%'),
                MarketProduct.district.ilike(f'%{query}%'),
                MarketProduct.mandi.ilike(f'%{query}%'),
                MarketProduct.description.ilike(f'%{query}%')
            )
        ).order_by(
            MarketProduct.is_verified.desc(),
            MarketProduct.created_at.desc()
        ).limit(limit).all()

        return jsonify({
            'success': True,
            'query': query,
            'results': [l.to_dict(language) for l in listings],
            'count': len(listings)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error searching: {str(e)}'
        }), 500


@market_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get marketplace statistics"""
    try:
        total = MarketProduct.query.count()
        active = MarketProduct.query.filter_by(status='available').count()
        verified = MarketProduct.query.filter_by(is_verified=True).count()
        sold = MarketProduct.query.filter_by(status='sold').count()

        # Crop-wise distribution
        crop_stats = db.session.query(
            MarketProduct.crop,
            func.count(MarketProduct.id)
        ).filter_by(status='available')\
         .group_by(MarketProduct.crop)\
         .order_by(func.count(MarketProduct.id).desc())\
         .limit(10).all()

        crop_data = {c: count for c, count in crop_stats if c}

        # District-wise distribution
        district_stats = db.session.query(
            MarketProduct.district,
            func.count(MarketProduct.id)
        ).filter_by(status='available')\
         .group_by(MarketProduct.district)\
         .order_by(func.count(MarketProduct.id).desc())\
         .limit(10).all()

        district_data = {d: count for d, count in district_stats if d}

        # Price stats
        price_stats = db.session.query(
            func.avg(MarketProduct.price_per_unit),
            func.min(MarketProduct.price_per_unit),
            func.max(MarketProduct.price_per_unit)
        ).filter(
            MarketProduct.status == 'available',
            MarketProduct.price_per_unit.isnot(None)
        ).first()

        avg_price, min_price, max_price = price_stats

        return jsonify({
            'success': True,
            'stats': {
                'total_listings': total,
                'active_listings': active,
                'verified_listings': verified,
                'sold_listings': sold,
                'by_crop': crop_data,
                'by_district': district_data,
                'price_stats': {
                    'average': round(avg_price, 2) if avg_price else 0,
                    'minimum': round(min_price, 2) if min_price else 0,
                    'maximum': round(max_price, 2) if max_price else 0
                },
                'verification_rate': round((verified / active * 100), 1) if active > 0 else 0
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching stats: {str(e)}'
        }), 500