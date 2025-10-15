# import os
# import time
# from pathlib import Path
# import glob

# def cleanup_old_segments(hls_dir, max_age_seconds=30):
#     """Delete .ts files older than max_age_seconds"""
#     while True:
#         try:
#             # Find all .ts files
#             ts_files = glob.glob(os.path.join(hls_dir, '**', '*.ts'), recursive=True)
#             current_time = time.time()
#             deleted_count = 0
            
#             for file_path in ts_files:
#                 file_age = current_time - os.path.getmtime(file_path)
#                 if file_age > max_age_seconds:
#                     try:
#                         os.remove(file_path)
#                         deleted_count += 1
#                         print(f"[CLEANUP] Deleted old segment: {os.path.basename(file_path)}")
#                     except Exception as e:
#                         print(f"[CLEANUP ERROR] {e}")
            
#             if deleted_count > 0:
#                 print(f"[CLEANUP] Removed {deleted_count} old segments")
                
#         except Exception as e:
#             print(f"[CLEANUP ERROR] {e}")
        
#         time.sleep(5)  # Run every 5 seconds

# if __name__ == '__main__':
#     HLS_DIR = r'C:\Users\Manveen\Desktop\new_things_to_mess_araound\Livesitter\backend\static\hls'
#     print(f"[CLEANUP] Starting segment cleaner for: {HLS_DIR}")
#     cleanup_old_segments(HLS_DIR, max_age_seconds=30)



# FIXED HLS Cleaner with Correct Path
import os
import time
import glob
import threading
from pathlib import Path
import logging

class OptimizedHLSCleaner:
    """Enhanced HLS segment cleaner with better performance and monitoring."""
    
    def __init__(self, hls_dir, max_age_seconds=30, check_interval=5):
        self.max_age_seconds = max_age_seconds
        self.check_interval = check_interval
        self.running = False
        self.thread = None
        self.stats = {
            'total_cleaned': 0,
            'last_cleanup': None,
            'errors': 0
        }
        
        # FIXED: Handle directory creation with proper error handling and fallback
        self.hls_dir = self._setup_hls_directory(hls_dir)
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def _setup_hls_directory(self, requested_dir):
        """Setup HLS directory with fallback options."""
        try:
            # Try the requested directory first
            Path(requested_dir).mkdir(parents=True, exist_ok=True)
            print(f"[CLEANER] Using requested directory: {requested_dir}")
            return requested_dir
        except PermissionError:
            print(f"[CLEANER WARNING] Permission denied for {requested_dir}")
            # Try current directory as fallback
            fallback_dir = os.path.join(os.getcwd(), 'static', 'hls')
            try:
                Path(fallback_dir).mkdir(parents=True, exist_ok=True)
                print(f"[CLEANER] Using fallback directory: {fallback_dir}")
                return fallback_dir
            except Exception as e:
                print(f"[CLEANER ERROR] Fallback failed: {e}")
                # Last resort: use temp directory
                import tempfile
                temp_dir = os.path.join(tempfile.gettempdir(), 'hls_output')
                Path(temp_dir).mkdir(parents=True, exist_ok=True)
                print(f"[CLEANER] Using temp directory: {temp_dir}")
                return temp_dir
        except Exception as e:
            print(f"[CLEANER ERROR] Failed to create directory {requested_dir}: {e}")
            # Use current directory as last resort
            current_dir = os.path.join(os.getcwd(), 'hls_output')
            Path(current_dir).mkdir(parents=True, exist_ok=True)
            print(f"[CLEANER] Using current directory: {current_dir}")
            return current_dir
    
    def start(self):
        """Start the OPTIMIZED cleaner in a background thread."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._optimized_cleanup_loop, daemon=True)
            self.thread.start()
            print(f"[OPTIMIZED CLEANER] Started for directory: {self.hls_dir}")
            print(f"[OPTIMIZED CLEANER] Settings: max_age={self.max_age_seconds}s, interval={self.check_interval}s")
    
    def stop(self):
        """Stop the OPTIMIZED cleaner."""
        if self.running:
            self.running = False
            if self.thread and self.thread.is_alive():
                self.thread.join()
            print("[OPTIMIZED CLEANER] Stopped")
    
    def _optimized_cleanup_loop(self):
        """Main OPTIMIZED cleanup loop with performance monitoring."""
        while self.running:
            try:
                cleanup_start = time.time()
                deleted_count = self._cleanup_old_segments()
                cleanup_duration = time.time() - cleanup_start
                
                if deleted_count > 0:
                    self.stats['total_cleaned'] += deleted_count
                    self.stats['last_cleanup'] = time.time()
                    print(f"[OPTIMIZED CLEANER] Cleaned {deleted_count} segments in {cleanup_duration:.2f}s")
                
                # Sleep for check interval
                time.sleep(self.check_interval)
                
            except Exception as e:
                self.stats['errors'] += 1
                print(f"[OPTIMIZED CLEANER ERROR] {e}")
                # Continue running even on errors
                time.sleep(self.check_interval)
    
    def _cleanup_old_segments(self):
        """Delete old .ts files with OPTIMIZED performance."""
        try:
            # Use more efficient glob pattern
            ts_pattern = os.path.join(self.hls_dir, '**', '*.ts')
            ts_files = glob.glob(ts_pattern, recursive=True)
            
            current_time = time.time()
            deleted_count = 0
            
            # Batch process files for better performance
            for file_path in ts_files:
                try:
                    # Check file age
                    file_age = current_time - os.path.getmtime(file_path)
                    
                    if file_age > self.max_age_seconds:
                        # Additional safety check - don't delete very recent files
                        if file_age > 10:  # At least 10 seconds old
                            os.remove(file_path)
                            deleted_count += 1
                            
                            # Log individual deletions in debug mode only
                            if hasattr(self, 'logger') and self.logger.isEnabledFor(logging.DEBUG):
                                self.logger.debug(f"[OPTIMIZED CLEANER] Deleted: {os.path.basename(file_path)} (age: {file_age:.1f}s)")
                    
                except (OSError, IOError) as e:
                    # File might be in use or already deleted
                    if hasattr(self, 'logger'):
                        self.logger.debug(f"[OPTIMIZED CLEANER] Could not delete {file_path}: {e}")
                    continue
                except Exception as e:
                    print(f"[OPTIMIZED CLEANER] Unexpected error with {file_path}: {e}")
                    continue
            
            return deleted_count
            
        except Exception as e:
            print(f"[OPTIMIZED CLEANER] Cleanup failed: {e}")
            return 0
    
    def cleanup_stream_directory(self, stream_id):
        """Clean up all files for a specific stream (OPTIMIZED)."""
        try:
            stream_dir = os.path.join(self.hls_dir, stream_id)
            if not os.path.exists(stream_dir):
                return 0
            
            # Get all files in stream directory
            files_to_delete = []
            for ext in ['*.ts', '*.m3u8']:
                files_to_delete.extend(glob.glob(os.path.join(stream_dir, ext)))
            
            deleted_count = 0
            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"[OPTIMIZED CLEANER] Could not delete {file_path}: {e}")
            
            # Try to remove empty directory
            try:
                if not os.listdir(stream_dir):
                    os.rmdir(stream_dir)
                    print(f"[OPTIMIZED CLEANER] Removed empty stream directory: {stream_id}")
            except:
                pass  # Directory not empty or other error
            
            if deleted_count > 0:
                print(f"[OPTIMIZED CLEANER] Cleaned up {deleted_count} files for stream: {stream_id}")
            
            return deleted_count
            
        except Exception as e:
            print(f"[OPTIMIZED CLEANER] Failed to clean stream directory {stream_id}: {e}")
            return 0
    
    def get_stats(self):
        """Get cleaner statistics."""
        return {
            'running': self.running,
            'total_cleaned': self.stats['total_cleaned'],
            'last_cleanup': self.stats['last_cleanup'],
            'errors': self.stats['errors'],
            'settings': {
                'max_age_seconds': self.max_age_seconds,
                'check_interval': self.check_interval,
                'hls_directory': self.hls_dir
            }
        }
    
    def get_directory_info(self):
        """Get information about HLS directory (OPTIMIZED)."""
        try:
            total_files = 0
            total_size = 0
            oldest_file = None
            newest_file = None
            
            # Efficiently scan directory
            for root, dirs, files in os.walk(self.hls_dir):
                for file in files:
                    if file.endswith(('.ts', '.m3u8')):
                        file_path = os.path.join(root, file)
                        try:
                            stat = os.stat(file_path)
                            total_files += 1
                            total_size += stat.st_size
                            
                            if oldest_file is None or stat.st_mtime < oldest_file:
                                oldest_file = stat.st_mtime
                            if newest_file is None or stat.st_mtime > newest_file:
                                newest_file = stat.st_mtime
                                
                        except:
                            continue
            
            return {
                'total_files': total_files,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'oldest_file_age': time.time() - oldest_file if oldest_file else 0,
                'newest_file_age': time.time() - newest_file if newest_file else 0
            }
            
        except Exception as e:
            print(f"[OPTIMIZED CLEANER] Failed to get directory info: {e}")
            return {'error': str(e)}
    
    def force_cleanup(self):
        """Force immediate cleanup of all old segments."""
        print("[OPTIMIZED CLEANER] Force cleanup requested")
        try:
            deleted_count = self._cleanup_old_segments()
            self.stats['total_cleaned'] += deleted_count
            self.stats['last_cleanup'] = time.time()
            print(f"[OPTIMIZED CLEANER] Force cleanup completed: {deleted_count} files deleted")
            return deleted_count
        except Exception as e:
            print(f"[OPTIMIZED CLEANER] Force cleanup failed: {e}")
            return 0

# FIXED Usage example with YOUR actual path
if __name__ == '__main__':
    # Setup logging for testing
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # CORRECTED: Use your actual project path
    HLS_DIR = r'C:\Users\Manveen\Desktop\new_things_to_mess_araound\Livesitter\backend\static\hls'
    
    print("=" * 60)
    print("TESTING OPTIMIZED HLS CLEANER - FIXED VERSION")
    print("=" * 60)
    print(f"Target directory: {HLS_DIR}")
    
    cleaner = OptimizedHLSCleaner(HLS_DIR, max_age_seconds=20, check_interval=3)
    
    try:
        # Start cleaner
        cleaner.start()
        
        # Show directory info
        info = cleaner.get_directory_info()
        print(f"Directory info: {info}")
        
        # Run for a short time
        print("Running cleaner for 30 seconds...")
        time.sleep(30)
        
        # Show stats
        stats = cleaner.get_stats()
        print(f"Cleaner stats: {stats}")
        
    except KeyboardInterrupt:
        print("\nStopping cleaner...")
    finally:
        cleaner.stop()
        print("Cleaner stopped.")