
# # PRODUCTION-GRADE Flask API with Fixed Streaming
# from flask import Flask, send_from_directory, request, jsonify, make_response
# from flask_cors import CORS
# from pymongo import MongoClient
# from stream_manager import ProductionStreamManager
# import os
# import logging
# import atexit
# from pathlib import Path
# import time
# # Add to top of app.py
# from pymongo import MongoClient
# from bson import ObjectId
# import json

# from datetime import datetime

# # MongoDB Connection
# try:
#     mongo_client = MongoClient('mongodb://localhost:27017/')
#     db = mongo_client['livestream_db']
#     overlays_collection = db['overlays']
#     print("✅ Connected to MongoDB")
# except Exception as e:
#     print(f"❌ MongoDB connection failed: {e}")
#     overlays_collection = None

# # Helper to serialize MongoDB ObjectId
# def serialize_overlay(overlay):
#     if overlay:
#         overlay['_id'] = str(overlay['_id'])
#     return overlay




# def create_production_app():
#     """Production-grade Flask application with fixed streaming"""
#     app = Flask(__name__)
    
#     # Configuration
#     app.config.update({
#         'SECRET_KEY': os.getenv('SECRET_KEY', 'production-secret-key'),
#         'DEBUG': os.getenv('FLASK_DEBUG', 'False') == 'True',
#         'MONGO_URI': os.getenv('MONGO_URI', 'mongodb://localhost:27017/rtsp_streaming_app'),
#         'HLS_OUTPUT_DIR': os.path.join(os.path.dirname(__file__), 'static', 'hls'),
#         'FFMPEG_PATH': os.getenv('FFMPEG_PATH', r'C:\ffmpeg\bin\ffmpeg.exe'),
#         'CORS_ORIGINS': os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(','),
#         'MAX_CONCURRENT_STREAMS': int(os.getenv('MAX_CONCURRENT_STREAMS', '10')),
#     })
    
#     # Ensure HLS directory exists
#     Path(app.config['HLS_OUTPUT_DIR']).mkdir(parents=True, exist_ok=True)
    
#     # Enhanced logging
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#         handlers=[
#             logging.StreamHandler(),
#             logging.FileHandler('streaming_app.log')
#         ]
#     )
#     logger = logging.getLogger(__name__)
    
#     # CORS configuration for streaming
#     # Replace your existing CORS(...) call with:
#     CORS(app, resources={
#         r"/api/*": {
#             "origins": app.Config.CORS_ORIGINS or "*",
#             "methods": ["GET","POST","PUT","DELETE","OPTIONS"],
#             "allow_headers": ["Content-Type","Range","Accept"],
#             "expose_headers": ["Accept-Ranges","Content-Length","Content-Range"]
#         },
#         r"/static/hls/*": {
#             "origins": "*",
#             "methods": ["GET","HEAD","OPTIONS"],
#             "allow_headers": ["Range","Accept"],
#             "expose_headers": ["Accept-Ranges","Content-Length","Content-Range"]
#         }
#     })

    
#     # MongoDB connection
#     try:
#         client = MongoClient(app.config['MONGO_URI'])
#         db_name = app.config['MONGO_URI'].split('/')[-1].split('?')[0]
#         app.db = client[db_name]
#         logger.info(f"Connected to MongoDB: {db_name}")
#     except Exception as e:
#         logger.error(f"MongoDB connection failed: {e}")
#         app.db = None
    
#     # Initialize PRODUCTION stream manager
#     app.stream_manager = ProductionStreamManager(
#         hls_output_dir=app.config['HLS_OUTPUT_DIR'],
#         ffmpeg_path=app.config['FFMPEG_PATH']
#     )

#     # Preflight for /api/stream/start, /api/stream/stop, etc.
#     @app.route('/api/stream/<path:path>', methods=['OPTIONS'])
#     def stream_options(path):
#         response = make_response('', 204)
#         response.headers.update({
#             'Access-Control-Allow-Origin': '*',
#             'Access-Control-Allow-Methods': 'GET,HEAD,POST,PUT,DELETE,OPTIONS',
#             'Access-Control-Allow-Headers': 'Content-Type,Range,Accept',
#             'Access-Control-Max-Age': '86400'
#         })
#         return response



#     # ====================== OVERLAY CRUD ENDPOINTS ======================

#     # Add this to your app.py - IMPROVED OVERLAY ENDPOINT

#     @app.route('/api/overlays', methods=['POST'])
#     def create_overlay():
#         """Create new overlay with better validation"""
#         try:
#             data = request.json
            
#             # Debug: Print what we received
#             print("📥 Received overlay data:", json.dumps(data, indent=2))
            
#             # Validate required fields
#             if not data:
#                 return jsonify({
#                     'success': False,
#                     'error': 'No data provided'
#                 }), 400
                
#             if 'type' not in data:
#                 return jsonify({
#                     'success': False,
#                     'error': 'Missing field: type'
#                 }), 400
                
#             if 'position' not in data or not isinstance(data['position'], dict):
#                 return jsonify({
#                     'success': False,
#                     'error': 'Missing or invalid field: position (must be object with x, y)'
#                 }), 400
                
#             if 'size' not in data or not isinstance(data['size'], dict):
#                 return jsonify({
#                     'success': False,
#                     'error': 'Missing or invalid field: size (must be object with width, height)'
#                 }), 400
            
#             # Create overlay document
#             overlay = {
#                 'type': data['type'],
#                 'content': data.get('content', ''),
#                 'position': {
#                     'x': data['position'].get('x', 10),
#                     'y': data['position'].get('y', 10)
#                 },
#                 'size': {
#                     'width': data['size'].get('width', 200),
#                     'height': data['size'].get('height', 50)
#                 },
#                 'style': data.get('style', {}),
#                 'visible': data.get('visible', True),
#                 'stream_id': data.get('stream_id', 'default'),
#                 'created_at': datetime.now().isoformat(),
#                 'updated_at': datetime.now().isoformat()
#             }
            
#             # Insert into MongoDB
#             result = overlays_collection.insert_one(overlay)
#             overlay['_id'] = str(result.inserted_id)
            
#             print("✅ Overlay created successfully:", overlay['_id'])
            
#             return jsonify({
#                 'success': True,
#                 'overlay': overlay
#             }), 201
            
#         except Exception as e:
#             print("❌ Error creating overlay:", str(e))
#             import traceback
#             traceback.print_exc()
#             return jsonify({
#                 'success': False,
#                 'error': str(e)
#             }), 500


#     @app.route('/api/overlays/<overlay_id>', methods=['GET'])
#     def get_overlay(overlay_id):
#         """Get single overlay by ID"""
#         try:
#             overlay = overlays_collection.find_one({'_id': ObjectId(overlay_id)})
#             if overlay:
#                 return jsonify({
#                     'success': True,
#                     'overlay': serialize_overlay(overlay)
#                 })
#             return jsonify({'success': False, 'error': 'Overlay not found'}), 404
#         except Exception as e:
#             return jsonify({'success': False, 'error': str(e)}), 500

  
#     @app.route('/api/overlays/<overlay_id>', methods=['PUT'])
#     def update_overlay(overlay_id):
#         """Update existing overlay"""
#         try:
#             data = request.json
#             data['updated_at'] = datetime.now().isoformat()
            
#             result = overlays_collection.update_one(
#                 {'_id': ObjectId(overlay_id)},
#                 {'$set': data}
#             )
            
#             if result.matched_count:
#                 overlay = overlays_collection.find_one({'_id': ObjectId(overlay_id)})
#                 return jsonify({
#                     'success': True,
#                     'overlay': serialize_overlay(overlay)
#                 })
#             return jsonify({'success': False, 'error': 'Overlay not found'}), 404
#         except Exception as e:
#             return jsonify({'success': False, 'error': str(e)}), 500

#     @app.route('/api/overlays/<overlay_id>', methods=['DELETE'])
#     def delete_overlay(overlay_id):
#         """Delete overlay"""
#         try:
#             result = overlays_collection.delete_one({'_id': ObjectId(overlay_id)})
#             if result.deleted_count:
#                 return jsonify({'success': True, 'message': 'Overlay deleted'})
#             return jsonify({'success': False, 'error': 'Overlay not found'}), 404
#         except Exception as e:
#             return jsonify({'success': False, 'error': str(e)}), 500

#     @app.route('/api/overlays/stream/<stream_id>', methods=['GET'])
#     def get_stream_overlays(stream_id):
#         """Get all overlays for a specific stream"""
#         try:
#             overlays = list(overlays_collection.find({'stream_id': stream_id, 'visible': True}))
#             return jsonify({
#                 'success': True,
#                 'overlays': [serialize_overlay(o) for o in overlays]
#             })
#         except Exception as e:
#             return jsonify({'success': False, 'error': str(e)}), 500
    
#     # HLS file serving with production optimizations
#     @app.route('/static/hls/<path:filename>')
#     def serve_hls(filename):
#         """Serve HLS files with production-grade headers and error handling"""
#         try:
#             # Extract stream_id from path
#             path_parts = filename.split('/')
#             if len(path_parts) < 2:
#                 return jsonify({'error': 'Invalid HLS path'}), 404
            
#             stream_id = path_parts[0]
#             file_name = '/'.join(path_parts[1:])
            
#             # Security: Validate stream exists
#             if stream_id not in app.stream_manager.sessions:
#                 logger.warning(f"Attempt to access non-existent stream: {stream_id}")
#                 return jsonify({'error': 'Stream not found'}), 404
            
#             # Determine MIME type and caching strategy
#             if file_name.endswith('.m3u8'):
#                 mimetype = 'application/vnd.apple.mpegurl'
#                 cache_control = 'no-cache, no-store, must-revalidate'
#                 max_age = 0
#             elif file_name.endswith('.ts'):
#                 mimetype = 'video/mp2t'  
#                 cache_control = 'public, max-age=86400'  # Cache segments for 24 hours
#                 max_age = 86400
#             else:
#                 mimetype = 'application/octet-stream'
#                 cache_control = 'public, max-age=3600'
#                 max_age = 3600
            
#             # Serve file with optimized headers
#             response = send_from_directory(
#                 app.config['HLS_OUTPUT_DIR'],
#                 filename,
#                 mimetype=mimetype
#             )
            
#             # Production headers for smooth streaming
#             response.headers.update({
#                 'Access-Control-Allow-Origin': '*',
#                 'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
#                 'Access-Control-Allow-Headers': 'Range, Content-Type, Accept, Origin',
#                 'Access-Control-Expose-Headers': 'Accept-Ranges, Content-Length, Content-Range',
#                 'Accept-Ranges': 'bytes',
#                 'Cache-Control': cache_control,
#                 'Expires': f'max-age={max_age}',
#                 'X-Content-Type-Options': 'nosniff',
#             })
            
#             # Add ETag for better caching
#             if file_name.endswith('.ts'):
#                 response.headers['ETag'] = f'"{stream_id}-{file_name}"'
            
#             return response
            
#         except FileNotFoundError:
#             logger.warning(f"HLS file not found: {filename}")
#             return jsonify({'error': 'File not found', 'filename': filename}), 404
#         except Exception as e:
#             logger.error(f"Error serving HLS file {filename}: {str(e)}")
#             return jsonify({'error': 'Internal server error'}), 500
    
#     @app.route('/static/hls/<path:filename>', methods=['OPTIONS'])
#     def serve_hls_options(filename):
#         """Handle CORS preflight for HLS files"""
#         response = make_response('', 204)
#         response.headers.update({
#             'Access-Control-Allow-Origin': '*',
#             'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
#             'Access-Control-Allow-Headers': 'Range, Content-Type, Accept, Origin',
#             'Access-Control-Max-Age': '86400',
#         })
#         return response
    
#     # API Endpoints
#     @app.route('/api/health', methods=['GET'])
#     def health_check():
#         """Enhanced health check with system status"""
#         active_streams = len(app.stream_manager.sessions)
#         return jsonify({
#             'status': 'healthy',
#             'service': 'Production RTSP Streaming API',
#             'version': '3.0.0',
#             'timestamp': int(time.time()),
#             'features': {
#                 'stream_isolation': True,
#                 'auto_recovery': True,
#                 'production_logging': True,
#                 'concurrent_streams': True,
#                 'overlay_management': True
#             },
#             'stats': {
#                 'active_streams': active_streams,
#                 'max_streams': app.config['MAX_CONCURRENT_STREAMS'],
#                 'mongodb_connected': app.db is not None
#             }
#         }), 200
    
#     @app.route('/api/streams', methods=['POST'])
#     def create_stream():
#         """Create a new stream with enhanced validation"""
#         try:
#             data = request.get_json()
#             if not data:
#                 return jsonify({'error': 'JSON body required'}), 400
            
#             # Validate required fields
#             rtsp_url = data.get('rtsp_url')
#             if not rtsp_url:
#                 return jsonify({'error': 'rtsp_url is required'}), 400
            
#             if not rtsp_url.startswith('rtsp://'):
#                 return jsonify({'error': 'Invalid RTSP URL format'}), 400
            
#             # Check concurrent stream limit
#             if len(app.stream_manager.sessions) >= app.config['MAX_CONCURRENT_STREAMS']:
#                 return jsonify({'error': 'Maximum concurrent streams reached'}), 429
            
#             # Optional parameters
#             stream_id = data.get('stream_id')   
#             force_mode = data.get('mode')  # 'local' or 'external' to override detection
            
#             # Start stream
#             result = app.stream_manager.start_stream(
#                 rtsp_url=rtsp_url,
#                 stream_id=None,
#                 force_mode=force_mode
#             )
            
#             if result.get('success'):
#                 logger.info(f"Stream created successfully: {result['stream_id']}")
                
#                 # Store stream metadata in MongoDB
#                 if app.db is not None:
#                     try:
#                         app.db.streams.insert_one({
#                             'stream_id': result['stream_id'],
#                             'rtsp_url': rtsp_url,
#                             'created_at': int(time.time()),
#                             'status': 'active'
#                         })
#                     except Exception as e:
#                         logger.warning(f"Failed to store stream metadata: {e}")
                
#                 return jsonify(result), 201
#             else:
#                 logger.error(f"Failed to create stream: {result.get('error')}")
#                 return jsonify(result), 500
                
#         except Exception as e:
#             logger.error(f"Stream creation error: {e}")
#             return jsonify({'error': 'Internal server error'}), 500
    
#     @app.route('/api/streams/<stream_id>', methods=['GET'])
#     def get_stream_status(stream_id):
#         """Get detailed stream status"""
#         try:
#             status = app.stream_manager.get_stream_status(stream_id)
#             if status.get('success') == False:
#                 return jsonify(status), 404
#             return jsonify(status), 200
#         except Exception as e:
#             logger.error(f"Error getting stream status: {e}")
#             return jsonify({'error': 'Internal server error'}), 500
    
#     @app.route('/api/streams', methods=['GET'])
#     def list_streams():
#         """List all active streams"""
#         try:
#             streams = app.stream_manager.get_all_streams()
#             return jsonify({
#                 'streams': streams,
#                 'count': len(streams),
#                 'max_concurrent': app.config['MAX_CONCURRENT_STREAMS']
#             }), 200
#         except Exception as e:
#             logger.error(f"Error listing streams: {e}")
#             return jsonify({'error': 'Internal server error'}), 500
    
#     @app.route('/api/streams/<stream_id>', methods=['DELETE'])
#     def delete_stream(stream_id):
#         """Stop and delete a stream"""
#         try:
#             result = app.stream_manager.stop_stream(stream_id)
            
#             # Remove from MongoDB
#             if app.db is not None:
#                 try:
#                     app.db.streams.delete_one({'stream_id': stream_id})
#                 except Exception as e:
#                     logger.warning(f"Failed to delete stream metadata: {e}")
            
#             if result.get('success'):
#                 logger.info(f"Stream deleted successfully: {stream_id}")
#                 return jsonify(result), 200
#             else:
#                 return jsonify(result), 404
                
#         except Exception as e:
#             logger.error(f"Error deleting stream: {e}")
#             return jsonify({'error': 'Internal server error'}), 500
    
#     @app.route('/api/streams/<stream_id>/restart', methods=['POST'])
#     def restart_stream(stream_id):
#         """Restart an existing stream"""
#         try:
#             result = app.stream_manager.restart_stream(stream_id)
            
#             if result.get('success'):
#                 logger.info(f"Stream restarted successfully: {stream_id}")
#                 return jsonify(result), 200
#             else:
#                 return jsonify(result), 404
                
#         except Exception as e:
#             logger.error(f"Error restarting stream: {e}")
#             return jsonify({'error': 'Internal server error'}), 500
    
#     # Overlay Management API (if MongoDB available)
#     if app.db is not None:
#         @app.route('/api/overlays', methods=['GET'])
#         def list_overlays():
#             """List all overlays"""
#             try:
#                 overlays = list(app.db.overlays.find({}, {'_id': 0}))
#                 return jsonify({'overlays': overlays, 'count': len(overlays)}), 200
#             except Exception as e:
#                 logger.error(f"Error listing overlays: {e}")
#                 return jsonify({'error': 'Internal server error'}), 500
        
        
#     # Sample RTSP URLs for testing
#     @app.route('/api/sample-streams', methods=['GET'])
#     def get_sample_streams():
#         """Get sample RTSP URLs for testing"""
#         samples = [
#             {
#                 'name': 'Big Buck Bunny',
#                 'rtsp_url': 'rtsp://rtspstream:_4yf2XfZ7H6BNI-tsTdWW@zephyr.rtsp.stream/movie',
#                 'description': 'High quality test stream',
#                 'type': 'external'
#             },
#             {
#                 'name': 'Traffic Camera',
#                 'rtsp_url': 'rtsp://rtspstream:_4yf2XfZ7H6BNI-tsTdWW@zephyr.rtsp.stream/traffic',
#                 'description': 'Live traffic camera feed',
#                 'type': 'external'
#             },
#             {
#                 'name': 'Local Test',
#                 'rtsp_url': 'rtsp://192.168.1.100:554/stream1',
#                 'description': 'Example local camera',
#                 'type': 'local'
#             }
#         ]
#         return jsonify({'samples': samples, 'count': len(samples)}), 200
    
#     # Error handlers
#     @app.errorhandler(400)
#     def bad_request(error):
#         return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
#     @app.errorhandler(404)
#     def not_found(error):
#         return jsonify({'error': 'Not found', 'message': 'The requested resource was not found'}), 404
    
#     @app.errorhandler(429)
#     def rate_limit_exceeded(error):
#         return jsonify({'error': 'Too many requests', 'message': 'Rate limit exceeded'}), 429
    
#     @app.errorhandler(500)
#     def internal_error(error):
#         logger.error(f"Internal server error: {str(error)}")
#         return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500
    
#     # Cleanup on shutdown
#     @atexit.register
#     def cleanup_streams():
#         """Cleanup all streams on application shutdown"""
#         logger.info("Application shutting down - cleaning up streams")
#         if hasattr(app, 'stream_manager'):
#             app.stream_manager.shutdown()


#     # Add AFTER your other imports, BEFORE routes
#     @app.after_request
#     def add_hls_headers(response):
#         """Add proper headers for HLS streaming"""
#         # Set CORS headers
#         response.headers['Access-Control-Allow-Origin'] = '*'
#         response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
#         response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
#         # Set proper content types for HLS files
#         if request.path.endswith('.m3u8'):
#             response.headers['Content-Type'] = 'application/vnd.apple.mpegurl'
#             response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#         elif request.path.endswith('.ts'):
#             response.headers['Content-Type'] = 'video/mp2t'
#             response.headers['Cache-Control'] = 'max-age=10'
        
#         return response


    
    
#     return app

# # Create the application instance
# def main():
#     """Main application entry point"""
#     app = create_production_app()
    
#     logger = logging.getLogger(__name__)
#     logger.info("=" * 70)
#     logger.info(" PRODUCTION RTSP TO HLS STREAMING SERVER")
#     logger.info("=" * 70)
#     logger.info(" Features enabled:")
#     logger.info("   • Complete stream isolation")
#     logger.info("   • Race condition fixes")
#     logger.info("   • Production error handling")
#     logger.info("   • Concurrent stream support")
#     logger.info("   • MongoDB overlay management")
#     logger.info("   • Comprehensive API")
#     logger.info("   • Health monitoring")
#     logger.info("=" * 70)
    
#     # Development vs Production
#     if app.config['DEBUG']:
#         logger.info("🔧 Running in DEVELOPMENT mode")
#         app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
#     else:
#         logger.info(" Running in PRODUCTION mode")
#         # Use production WSGI server
#         try:
#             from waitress import serve
#             serve(app, host='0.0.0.0', port=5000, threads=8)
#         except ImportError:
#             logger.warning("Waitress not available, using development server")
#             app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

# if __name__ == '__main__':
#     main()




import os
import logging
from datetime import datetime
from flask import Flask, send_from_directory, request, jsonify, make_response
from flask_cors import CORS
from pymongo import MongoClient
from routes.overlays import overlays_bp, init_overlays_routes
from stream_manager import ProductionStreamManager
from cleaner import OptimizedHLSCleaner

# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------
class Config:
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "prod-secret")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/rtsp_streaming_app")
    HLS_OUTPUT_DIR = os.getenv("HLS_OUTPUT_DIR", "./static/hls")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

# -----------------------------------------------------------------------------
# APPLICATION FACTORY
# -----------------------------------------------------------------------------
def create_app():
    app = Flask(__name__, static_folder="static")
    app.config.from_object(Config)

    # Logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logger = logging.getLogger(__name__)

    # CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config["CORS_ORIGINS"],
            "methods": ["GET","POST","PUT","DELETE","OPTIONS"],
            "allow_headers": ["Content-Type","Range","Accept"],
            "expose_headers": ["Accept-Ranges","Content-Length","Content-Range"]
        },
        r"/static/hls/*": {
            "origins": "*",
            "methods": ["GET","HEAD","OPTIONS"],
            "allow_headers": ["Range","Accept"],
            "expose_headers": ["Accept-Ranges","Content-Length","Content-Range"]
        }
    })

    # MongoDB
    client = MongoClient(app.config["MONGO_URI"])
    db_name = app.config["MONGO_URI"].rsplit("/",1)[-1].split("?")[0]
    db = client[db_name]
    logger.info(f"Connected to MongoDB: {db_name}")

    # Overlay routes
    init_overlays_routes(db)
    app.register_blueprint(overlays_bp)

    # Stream manager
    app.stream_manager = ProductionStreamManager(app.config["HLS_OUTPUT_DIR"])

    # Serve HLS files
    @app.route("/static/hls/<path:filename>", methods=["GET"])
    def serve_hls(filename):
        try:
            if filename.endswith(".m3u8"):
                mimetype, cache = "application/vnd.apple.mpegurl", "no-cache, no-store, must-revalidate"
            elif filename.endswith(".ts"):
                mimetype, cache = "video/mp2t", "public, max-age=31536000"
            else:
                mimetype, cache = "application/octet-stream", "public, max-age=3600"
            resp = send_from_directory(app.config["HLS_OUTPUT_DIR"], filename, mimetype=mimetype)
            resp.headers.update({
                "Access-Control-Allow-Origin":"*",
                "Access-Control-Allow-Methods":"GET,HEAD,OPTIONS",
                "Access-Control-Allow-Headers":"Range,Content-Type,Accept",
                "Accept-Ranges":"bytes",
                "Cache-Control":cache
            })
            return resp
        except FileNotFoundError:
            logger.warning(f"HLS file not found: {filename}")
            return jsonify({"error":"File not found"}),404
        except Exception as e:
            logger.error(f"Error serving HLS: {e}")
            return jsonify({"error":"Internal server error"}),500

    # Preflight for stream endpoints
    @app.route("/api/stream/<path:path>", methods=["OPTIONS"])
    def stream_options(path):
        resp = make_response("",204)
        resp.headers.update({
            "Access-Control-Allow-Origin":"*",
            "Access-Control-Allow-Methods":"GET,HEAD,POST,PUT,DELETE,OPTIONS",
            "Access-Control-Allow-Headers":"Content-Type,Range,Accept",
            "Access-Control-Max-Age":"86400"
        })
        return resp

    # Health check
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status":"ok","service":"RTSP-HLS-API","version":"1.0"}),200

    # Start stream
    @app.route("/api/stream/start", methods=["POST"])
    def start_stream():
        data=request.json or {}
        url=data.get("rtsp_url","")
        if not url.startswith("rtsp://"):
            return jsonify({"error":"Invalid RTSP URL"}),400
        res=app.stream_manager.start_stream(url,stream_id=data.get("stream_id"))
        return jsonify(res), (200 if res.get("success") else 500)

    # Stream status
    @app.route("/api/stream/status", methods=["GET"])
    @app.route("/api/stream/status/<stream_id>", methods=["GET"])
    def stream_status(stream_id=None):
        return jsonify(app.stream_manager.get_stream_status(stream_id)),200

    # Stop stream
    @app.route("/api/stream/stop", methods=["POST"])
    def stop_stream():
        data=request.json or {}
        res=app.stream_manager.stop_stream(data.get("stream_id"))
        return jsonify(res), (200 if res.get("success") else 404)

    # Restart stream
    @app.route("/api/stream/restart", methods=["POST"])
    def restart_stream():
        data=request.json or {}
        url=data.get("rtsp_url","")
        if not url.startswith("rtsp://"):
            return jsonify({"error":"RTSP URL required"}),400
        res=app.stream_manager.restart_stream(url,stream_id=data.get("stream_id"))
        return jsonify(res), (200 if res.get("success") else 500)

    # List streams
    @app.route("/api/streams", methods=["GET"])
    def list_streams():
        return jsonify(app.stream_manager.list_streams()),200

    # Sample URLs
    @app.route("/api/sample-urls", methods=["GET"])
    def samples():
        return jsonify([
            {"name":"Demo Pattern","url":"rtsp://demo:demo@rtsp.stream/pattern"},
            {"name":"Big Buck Bunny","url":"rtsp://rtsp.stream/pattern"}
        ]),200

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error":"Endpoint not found"}),404

    @app.errorhandler(500)
    def internal(e):
        logger.error(f"Internal error: {e}")
        return jsonify({"error":"Internal server error"}),500

    return app

# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
if __name__=="__main__":
    app = create_app()
    cleaner = OptimizedHLSCleaner(app.config["HLS_OUTPUT_DIR"],max_age_seconds=30,check_interval=5)
    cleaner.start()
    logging.getLogger(__name__).info("HLS cleaner started")
    app.run(host="0.0.0.0",port=5000,debug=app.config["DEBUG"])
