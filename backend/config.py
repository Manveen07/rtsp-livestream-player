# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     """Flask configuration variables."""
    
#     # Flask settings
#     SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
#     DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
#     # MongoDB settings
#     MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/rtsp_overlay_app')
    
#     # RTSP/HLS settings
#     HLS_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'hls')
#     # DEFAULT_RTSP_URL = os.getenv('DEFAULT_RTSP_URL', '')
    
#     # CORS settings
#     CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')



# FIXED Configuration with Correct Paths
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Enhanced Flask configuration for OPTIMIZED RTSP to HLS streaming - FIXED PATHS."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # MongoDB settings
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/rtsp_overlay_app')
    
    # FIXED: Use your actual project path structure
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    HLS_OUTPUT_DIR = os.path.join(BASE_DIR, 'static', 'hls')
    
    # OPTIMIZED RTSP/HLS settings - KEY PERFORMANCE CONFIGURATIONS
    HLS_SEGMENT_DURATION = 2          # OPTIMIZED: 2-second segments (reduced from 5)
    HLS_PLAYLIST_SIZE = 6             # OPTIMIZED: Keep 6 segments (increased from 3)  
    HLS_DELETE_THRESHOLD = 30         # Delete segments older than 30 seconds
    
    # CORS settings - Enhanced for streaming
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
    
    # Performance settings - OPTIMIZED for smooth streaming
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024     # 32MB max file upload
    SEND_FILE_MAX_AGE_DEFAULT = 0              # Disable caching for development
    
    # Streaming optimization settings - NEW FEATURES
    STREAM_TIMEOUT = 30                        # Stream timeout in seconds
    MAX_CONCURRENT_STREAMS = 5                 # Maximum concurrent streams
    ENABLE_STREAM_MONITORING = True            # Enable health monitoring
    AUTO_RESTART_ON_FAILURE = True             # Auto-restart failed streams
    
    # Buffer management - OPTIMIZED for low latency
    BUFFER_SIZE = 8192                         # Buffer size for file operations
    CHUNK_SIZE = 1024                          # Chunk size for streaming
    
    # FFmpeg optimization settings - CORRECTED for your system
    FFMPEG_PATH = r'C:\ffmpeg\bin\ffmpeg.exe'  # FIXED: Update this path for your system
    FFMPEG_THREAD_COUNT = 2                    # Number of encoding threads
    FFMPEG_PRESET = 'ultrafast'                # Encoding preset
    FFMPEG_TUNE = 'zerolatency'                # Encoding tune
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Development settings
    DEVELOPMENT_MODE = DEBUG
    ENABLE_DEBUG_INFO = DEBUG                  # Show debug info in video player
    
    # Security settings
    ALLOWED_RTSP_HOSTS = os.getenv('ALLOWED_RTSP_HOSTS', '').split(',') if os.getenv('ALLOWED_RTSP_HOSTS') else []
    ENABLE_RATE_LIMITING = os.getenv('ENABLE_RATE_LIMITING', 'True') == 'True'
    
    # FIXED: Ensure directories exist on startup
    @classmethod
    def create_directories(cls):
        """Create necessary directories on startup."""
        try:
            # Create HLS output directory
            os.makedirs(cls.HLS_OUTPUT_DIR, exist_ok=True)
            print(f"[CONFIG] HLS directory ensured: {cls.HLS_OUTPUT_DIR}")
            
            # Create static directory if it doesn't exist
            static_dir = os.path.join(cls.BASE_DIR, 'static')
            os.makedirs(static_dir, exist_ok=True)
            print(f"[CONFIG] Static directory ensured: {static_dir}")
            
        except Exception as e:
            print(f"[CONFIG ERROR] Failed to create directories: {e}")
            # Use fallback directory
            fallback_dir = os.path.join(os.getcwd(), 'hls_output')
            os.makedirs(fallback_dir, exist_ok=True)
            cls.HLS_OUTPUT_DIR = fallback_dir
            print(f"[CONFIG] Using fallback HLS directory: {fallback_dir}")

# Create directories when config is imported
Config.create_directories()