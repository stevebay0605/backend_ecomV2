"""
Custom storage backend for ImgBB
Simple alternative to Cloudinary - no configuration needed
"""
import base64
import requests
from django.core.files.storage import Storage
from django.conf import settings
from django.core.files.base import ContentFile
import os


class ImgBBStorage(Storage):
    """
    Storage backend using ImgBB API
    Free tier: Unlimited uploads
    Get API key: https://api.imgbb.com/
    """
    
    def __init__(self):
        self.api_key = os.environ.get('IMGBB_API_KEY', '')
        self.api_url = 'https://api.imgbb.com/1/upload'
    
    def _save(self, name, content):
        """Upload file to ImgBB and return the public URL"""
        if not self.api_key:
            # Fallback to local storage if no API key
            return name
        
        try:
            # Read file content
            content.seek(0)
            file_data = content.read()
            
            # Encode to base64
            encoded = base64.b64encode(file_data).decode('utf-8')
            
            # Upload to ImgBB
            response = requests.post(
                self.api_url,
                data={
                    'key': self.api_key,
                    'image': encoded,
                    'name': os.path.basename(name)
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                # Return the full URL
                return data['data']['url']
            else:
                print(f"❌ ImgBB upload failed: {response.text}")
                return name
                
        except Exception as e:
            print(f"❌ ImgBB error: {e}")
            return name
    
    def url(self, name):
        """Return the URL - ImgBB returns full URLs"""
        if name and name.startswith('http'):
            return name
        return f'/media/{name}'
    
    def exists(self, name):
        """Check if file exists"""
        return name.startswith('http')
    
    def delete(self, name):
        """Delete not supported"""
        pass
    
    def size(self, name):
        """Size not tracked"""
        return 0
