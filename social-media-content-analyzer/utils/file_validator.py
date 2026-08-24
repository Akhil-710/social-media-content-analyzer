import os
from werkzeug.datastructures import FileStorage
import mimetypes


class FileValidator:
    """
    Validates uploaded files before processing.
    Checks file type, size, and content.
    """

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}

    # Allowed MIME types
    ALLOWED_MIMETYPES = {
        'application/pdf',
        'image/jpeg',
        'image/jpg',
        'image/png'
    }

    # Maximum file size (10 MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024

    def __init__(self):
        """Initialize file validator."""
        pass

    def validate(self, file: FileStorage) -> dict:
        """
        Validate an uploaded file.

        Args:
            file (FileStorage): The uploaded file object

        Returns:
            dict: {'valid': bool, 'error': str or None}
        """
        # Check if file exists
        if not file or file.filename == '':
            return {'valid': False, 'error': 'No file provided.'}

        # Check file extension
        extension_check = self._check_extension(file.filename)
        if not extension_check['valid']:
            return extension_check

        # Check file size
        size_check = self._check_file_size(file)
        if not size_check['valid']:
            return size_check

        # Check MIME type
        mimetype_check = self._check_mimetype(file)
        if not mimetype_check['valid']:
            return mimetype_check

        # Check if file is empty
        empty_check = self._check_empty_file(file)
        if not empty_check['valid']:
            return empty_check

        return {'valid': True, 'error': None}

    def _check_extension(self, filename: str) -> dict:
        """
        Check if file extension is allowed.

        Args:
            filename (str): The filename

        Returns:
            dict: Validation result
        """
        if not filename:
            return {'valid': False, 'error': 'Invalid filename.'}

        # Get file extension
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        if ext not in self.ALLOWED_EXTENSIONS:
            allowed = ', '.join(self.ALLOWED_EXTENSIONS)
            return {
                'valid': False,
                'error': f'Unsupported file type. Allowed formats: {allowed}'
            }

        return {'valid': True, 'error': None}

    def _check_file_size(self, file: FileStorage) -> dict:
        """
        Check if file size is within limits.

        Args:
            file (FileStorage): The uploaded file

        Returns:
            dict: Validation result
        """
        # Seek to end to get file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset to beginning

        if file_size == 0:
            return {'valid': False, 'error': 'File is empty. Please upload a valid file.'}

        if file_size > self.MAX_FILE_SIZE:
            return {
                'valid': False,
                'error': f'File is too large. Maximum size is 10 MB. Your file is {self._format_size(file_size)}.'
            }

        return {'valid': True, 'error': None}

    def _check_mimetype(self, file: FileStorage) -> dict:
        """
        Check if file MIME type is allowed.

        Args:
            file (FileStorage): The uploaded file

        Returns:
            dict: Validation result
        """
        # Get MIME type from filename
        mimetype, _ = mimetypes.guess_type(file.filename)

        if mimetype and mimetype not in self.ALLOWED_MIMETYPES:
            return {
                'valid': False,
                'error': 'File type not supported. Please use PDF, JPG, JPEG, or PNG.'
            }

        return {'valid': True, 'error': None}

    def _check_empty_file(self, file: FileStorage) -> dict:
        """
        Check if file has readable content.

        Args:
            file (FileStorage): The uploaded file

        Returns:
            dict: Validation result
        """
        # Read first few bytes to verify it's not corrupted
        try:
            file.seek(0)
            first_bytes = file.read(10)
            file.seek(0)

            if not first_bytes:
                return {'valid': False, 'error': 'File appears to be empty or corrupted.'}

            return {'valid': True, 'error': None}
        except Exception as e:
            return {'valid': False, 'error': f'Error reading file: {str(e)}'}

    def _format_size(self, size_bytes: int) -> str:
        """
        Format byte size to human-readable format.

        Args:
            size_bytes (int): Size in bytes

        Returns:
            str: Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"