"""
Simple caching mechanism for API responses
"""
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict

class CacheManager:
    """
    Simple file-based cache for API responses
    """
    
    def __init__(self, cache_dir: str = 'cache', ttl: int = 3600):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Directory to store cache files
            ttl: Time to live in seconds (default 1 hour)
        """
        self.cache_dir = cache_dir
        self.ttl = ttl
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def _get_cache_path(self, key: str) -> str:
        """Get file path for cache key"""
        safe_key = key.replace(':', '_').replace('.', '_')
        return os.path.join(self.cache_dir, f"{safe_key}.json")
    
    def get(self, key: str) -> Optional[Dict]:
        """
        Get cached data
        
        Args:
            key: Cache key (usually IP address)
            
        Returns:
            Cached data or None if not found/expired
        """
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cache is expired
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.utcnow() - cached_time > timedelta(seconds=self.ttl):
                # Cache expired, delete it
                os.remove(cache_path)
                return None
            
            return cache_data['data']
        
        except (json.JSONDecodeError, KeyError, ValueError):
            # Invalid cache file, delete it
            if os.path.exists(cache_path):
                os.remove(cache_path)
            return None
    
    def set(self, key: str, data: Dict) -> bool:
        """
        Set cached data
        
        Args:
            key: Cache key
            data: Data to cache
            
        Returns:
            bool: True if successful
        """
        cache_path = self._get_cache_path(key)
        
        try:
            cache_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'data': data
            }
            
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            return True
        
        except Exception as e:
            print(f"Cache write error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete cached data
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if deleted
        """
        cache_path = self._get_cache_path(key)
        
        if os.path.exists(cache_path):
            os.remove(cache_path)
            return True
        
        return False
    
    def clear(self) -> int:
        """
        Clear all cache
        
        Returns:
            int: Number of files deleted
        """
        count = 0
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.json'):
                os.remove(os.path.join(self.cache_dir, filename))
                count += 1
        return count

# Global cache instance
cache_manager = CacheManager()
