from datetime import datetime
from bson import ObjectId

class OverlayModel:
    """Helper class for overlay document operations."""
    
    @staticmethod
    def validate_overlay(data):
        """Validate overlay data before insert/update."""
        required_fields = ['type', 'content', 'xPercent', 'yPercent', 'widthPercent', 'heightPercent']
        
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Type validation
        if data['type'] not in ['text', 'image']:
            return False, "Type must be 'text' or 'image'"
        
        # Percent validation (0-100)
        percent_fields = ['xPercent', 'yPercent', 'widthPercent', 'heightPercent']
        for field in percent_fields:
            try:
                value = float(data[field])
                if value < 0 or value > 100:
                    return False, f"{field} must be between 0 and 100"
            except (ValueError, TypeError):
                return False, f"{field} must be a number"
        
        return True, None
    
    @staticmethod
    def create_overlay_doc(data):
        """Create a new overlay document with defaults."""
        return {
            'name': data.get('name', f"{data['type'].capitalize()} overlay"),
            'type': data['type'],
            'content': data['content'],
            'xPercent': float(data['xPercent']),
            'yPercent': float(data['yPercent']),
            'widthPercent': float(data['widthPercent']),
            'heightPercent': float(data['heightPercent']),
            'zIndex': int(data.get('zIndex', 5)),
            'visible': data.get('visible', True),
            'created_at': datetime.utcnow()
        }
    
    @staticmethod
    def serialize_overlay(doc):
        """Convert MongoDB document to JSON-serializable dict."""
        if doc is None:
            return None
        
        doc['_id'] = str(doc['_id'])
        if 'created_at' in doc:
            doc['created_at'] = doc['created_at'].isoformat()
        
        return doc
