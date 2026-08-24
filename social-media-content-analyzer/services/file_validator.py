# ==========================================================================
# File Validator Service
# Validates uploaded files for type, size, and integrity
# ==========================================================================

import os
from werkzeug.utils import secure_filename

class FileValidator:
    """Validates uploaded files before processing."""
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Maximum file size (10 MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    # MIME type mapping
    ALLOWED_MIMETYPES = {
        'application/pdf': 'pdf',
        'image/png': 'png',
        'image/jpeg': 'jpg',
        'image/gif': 'gif',
        'image/webp': 'webp'
    }
    
    def validate(self, file):
        """
        Validate uploaded file.
        
        Args:
            file: FileStorage object from Flask request
            
        Returns:
            dict: {'valid': bool, 'error': str or None}
        """
        try:
            # Check if file exists
            if not file:
                return {'valid': False, 'error': 'No file provided'}
            
            # Check filename
            if not file.filename:
                return {'valid': False, 'error': 'No filename provided'}
            
            # Check file extension
            if not self._check_extension(file.filename):
                return {
                    'valid': False,
                    'error': f'Invalid file type. Allowed types: {", ".join(self.ALLOWED_EXTENSIONS)}'
                }
            
            # Check MIME type
            if file.content_type not in self.ALLOWED_MIMETYPES:
                return {
                    'valid': False,
                    'error': f'Invalid MIME type: {file.content_type}'
                }
            
            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > self.MAX_FILE_SIZE:
                return {
                    'valid': False,
                    'error': f'File too large. Maximum size is {self.MAX_FILE_SIZE / (1024*1024):.0f} MB'
                }
            
            if file_size == 0:
                return {'valid': False, 'error': 'File is empty'}
            
            return {'valid': True, 'error': None}
        
        except Exception as e:
            return {'valid': False, 'error': f'Validation error: {str(e)}'}
    
    def _check_extension(self, filename):
        """Check if file extension is allowed."""
        if '.' not in filename:
            return False
        
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in self.ALLOWED_EXTENSIONS