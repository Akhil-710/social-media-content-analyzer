# ==========================================================================
# OCR Service
# Extracts text from images and scanned PDFs using Tesseract OCR
# ==========================================================================

import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import sys
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class OCRService:
    """
    Performs Optical Character Recognition on images and scanned PDFs.
    Uses Tesseract OCR engine.
    """

    def __init__(self):
        """Initialize OCR service and configure Tesseract path if needed."""
        # Check if Tesseract path is set in environment
        tesseract_path = os.getenv('TESSERACT_PATH')
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.pytesseract_cmd = tesseract_path

    def extract(self, filepath: str) -> Optional[str]:
        """
        Extract text from image file using OCR.

        Args:
            filepath (str): Path to image file

        Returns:
            Optional[str]: Extracted text or None if extraction fails
        """
        try:
            # Open image
            image = Image.open(filepath)

            # Convert to RGB if necessary (for PNG with transparency)
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')

            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(image)

            if not extracted_text or extracted_text.strip() == '':
                return None

            return extracted_text.strip()

        except pytesseract.TesseractNotFoundError:
            print("Error: Tesseract OCR is not installed or not found in PATH.", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Error extracting text from image: {str(e)}", file=sys.stderr)
            return None

    def extract_from_pdf(self, filepath: str) -> Optional[str]:
        """
        Extract text from scanned PDF using OCR.
        Used as fallback when regular PDF text extraction fails.

        Args:
            filepath (str): Path to PDF file

        Returns:
            Optional[str]: Extracted text or None if extraction fails
        """
        try:
            doc = fitz.open(filepath)
            extracted_text = []

            for page_num in range(doc.page_count):
                try:
                    # Render page to image
                    page = doc[page_num]
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
                    
                    # Convert pixmap to PIL Image
                    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                    # Extract text using OCR
                    text = pytesseract.image_to_string(image)

                    if text.strip():
                        extracted_text.append(text)

                except Exception as e:
                    print(f"Warning: OCR failed on page {page_num + 1}: {str(e)}", file=sys.stderr)
                    continue

            doc.close()

            if not extracted_text:
                return None

            full_text = "\n\n".join(extracted_text)
            return full_text if full_text.strip() else None

        except pytesseract.TesseractNotFoundError:
            print("Error: Tesseract OCR is not installed or not found in PATH.", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Error extracting text from PDF with OCR: {str(e)}", file=sys.stderr)
            return None

    def get_confidence(self, filepath: str) -> dict:
        """
        Get OCR confidence metrics for an image.

        Args:
            filepath (str): Path to image file

        Returns:
            dict: Confidence data from Tesseract
        """
        try:
            image = Image.open(filepath)

            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')

            # Get detailed data
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

            return {
                'confidence': float(sum(int(c) for c in data['conf'] if int(c) > 0) / len(data['conf'])) if data['conf'] else 0,
                'text_found': len([c for c in data['conf'] if int(c) > 0]) > 0
            }

        except Exception as e:
            print(f"Error getting OCR confidence: {str(e)}", file=sys.stderr)
            return {'confidence': 0, 'text_found': False}
            