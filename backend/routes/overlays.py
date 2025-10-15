from flask import Blueprint, request, jsonify
from bson import ObjectId
from models.overlay import OverlayModel

overlays_bp = Blueprint('overlays', __name__)

# MongoDB collection will be injected
db = None

def init_overlays_routes(mongo_db):
    """Initialize routes with MongoDB connection."""
    global db
    db = mongo_db

@overlays_bp.route('/api/overlays', methods=['GET'])
def get_overlays():
    """Get all overlays."""
    try:
        overlays = list(db.overlays.find())
        return jsonify([OverlayModel.serialize_overlay(o) for o in overlays]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@overlays_bp.route('/api/overlays/<overlay_id>', methods=['GET'])
def get_overlay(overlay_id):
    """Get single overlay by ID."""
    try:
        overlay = db.overlays.find_one({'_id': ObjectId(overlay_id)})
        if not overlay:
            return jsonify({'error': 'Overlay not found'}), 404
        
        return jsonify(OverlayModel.serialize_overlay(overlay)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@overlays_bp.route('/api/overlays', methods=['POST'])
def create_overlay():
    """Create new overlay."""
    try:
        data = request.get_json()
        
        # Validate
        is_valid, error_msg = OverlayModel.validate_overlay(data)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Create document
        overlay_doc = OverlayModel.create_overlay_doc(data)
        
        # Insert
        result = db.overlays.insert_one(overlay_doc)
        overlay_doc['_id'] = result.inserted_id
        
        return jsonify(OverlayModel.serialize_overlay(overlay_doc)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@overlays_bp.route('/api/overlays/<overlay_id>', methods=['PUT'])
def update_overlay(overlay_id):
    """Update existing overlay."""
    try:
        data = request.get_json()
        
        # Build update document (only update provided fields)
        update_fields = {}
        allowed_fields = ['name', 'type', 'content', 'xPercent', 'yPercent', 
                         'widthPercent', 'heightPercent', 'zIndex', 'visible']
        
        for field in allowed_fields:
            if field in data:
                update_fields[field] = data[field]
        
        if not update_fields:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        # Update
        result = db.overlays.update_one(
            {'_id': ObjectId(overlay_id)},
            {'$set': update_fields}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Overlay not found'}), 404
        
        # Return updated document
        updated_overlay = db.overlays.find_one({'_id': ObjectId(overlay_id)})
        return jsonify(OverlayModel.serialize_overlay(updated_overlay)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@overlays_bp.route('/api/overlays/<overlay_id>', methods=['DELETE'])
def delete_overlay(overlay_id):
    """Delete overlay."""
    try:
        result = db.overlays.delete_one({'_id': ObjectId(overlay_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Overlay not found'}), 404
        
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 400
