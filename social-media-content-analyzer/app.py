import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Import our custom services
from services.file_validator import FileValidator
from services.pdf_extractor import PDFExtractor
from services.ocr_service import OCRService
from services.content_analyzer import ContentAnalyzer
from services.suggestion_engine import SuggestionEngine
from utils.text_utils import clean_text

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10 MB
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize services
file_validator = FileValidator()
pdf_extractor = PDFExtractor()
ocr_service = OCRService()
content_analyzer = ContentAnalyzer()
suggestion_engine = SuggestionEngine()


@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'}), 200


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Main API endpoint to analyze uploaded files.
    Accepts PDF and image files.
    Returns analysis results and suggestions.
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided. Please upload a PDF or image file.'
            }), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected. Please choose a file.'
            }), 400

        # Validate file
        validation_result = file_validator.validate(file)
        if not validation_result['valid']:
            return jsonify({
                'success': False,
                'error': validation_result['error']
            }), 400

        # Secure filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save file temporarily
        file.save(filepath)

        try:
            # Determine file type and extract text
            file_extension = os.path.splitext(filename)[1].lower()

            if file_extension == '.pdf':
                # Try PDF extraction first
                extracted_text = pdf_extractor.extract(filepath)

                # If extraction yields little text, try OCR fallback for scanned PDFs
                if not extracted_text or len(extracted_text.strip()) < 50:
                    extracted_text = ocr_service.extract_from_pdf(filepath)

                if not extracted_text:
                    return jsonify({
                        'success': False,
                        'error': 'Could not extract text from PDF. It might be corrupted or empty.'
                    }), 400

            elif file_extension in ['.jpg', '.jpeg', '.png']:
                # Extract text from image using OCR
                extracted_text = ocr_service.extract(filepath)

                if not extracted_text:
                    return jsonify({
                        'success': False,
                        'error': 'Could not extract text from image. Try a clearer image.'
                    }), 400
            else:
                return jsonify({
                    'success': False,
                    'error': 'Unsupported file type. Please use PDF, JPG, JPEG, or PNG.'
                }), 400

            # Clean extracted text
            cleaned_text = clean_text(extracted_text)

            if not cleaned_text:
                return jsonify({
                    'success': False,
                    'error': 'Extracted text appears to be empty. Please try another file.'
                }), 400

            # Analyze content
            analysis = content_analyzer.analyze(cleaned_text)

            # Generate suggestions
            suggestions = suggestion_engine.generate(cleaned_text, analysis)

            # Return success response
            return jsonify({
                'success': True,
                'text': cleaned_text,
                'analysis': analysis,
                'suggestions': suggestions
            }), 200

        finally:
            # Clean up temporary file
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Warning: Could not delete temporary file {filepath}: {e}")

    except Exception as e:
        print(f"Error in /api/analyze: {str(e)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred. Please try again.'
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({
        'success': False,
        'error': 'File is too large. Maximum size is 10 MB.'
    }), 413


@app.errorhandler(500)
def internal_server_error(error):
    """Handle internal server error."""
    return jsonify({
        'success': False,
        'error': 'Server error occurred. Please try again.'
    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)