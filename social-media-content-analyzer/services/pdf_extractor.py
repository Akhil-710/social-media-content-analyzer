# ==========================================================================
# PDF Extractor Service
# Extracts text from PDF files using PyMuPDF
# ==========================================================================

import fitz  # PyMuPDF
import sys
from typing import Optional


class PDFExtractor:
    """
    Extracts text from PDF files using PyMuPDF (fitz).
    Handles multi-page PDFs and gracefully manages extraction errors.
    """

    def __init__(self):
        """Initialize PDF extractor."""
        pass

    def extract(self, filepath: str) -> Optional[str]:
        """
        Extract text from a PDF file.

        Args:
            filepath (str): Path to the PDF file

        Returns:
            Optional[str]: Extracted text or None if extraction fails
        """
        try:
            # Open PDF document
            doc = fitz.open(filepath)

            if doc.page_count == 0:
                print("PDF has no pages.", file=sys.stderr)
                return None

            extracted_text = []

            # Extract text from each page
            for page_num in range(doc.page_count):
                try:
                    page = doc[page_num]
                    text = page.get_text()
                    if text.strip():
                        extracted_text.append(text)
                except Exception as e:
                    print(f"Warning: Error extracting page {page_num + 1}: {str(e)}", file=sys.stderr)
                    continue

            doc.close()

            if not extracted_text:
                return None

            # Join all pages with newlines
            full_text = "\n\n".join(extracted_text)
            return full_text if full_text.strip() else None

        except fitz.FileError:
            print("Error: PDF file is corrupted or invalid.", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Error extracting PDF: {str(e)}", file=sys.stderr)
            return None

    def extract_metadata(self, filepath: str) -> dict:
        """
        Extract metadata from PDF.

        Args:
            filepath (str): Path to the PDF file

        Returns:
            dict: Metadata information
        """
        try:
            doc = fitz.open(filepath)
            metadata = {
                'page_count': doc.page_count,
                'title': doc.metadata.get('title', 'Unknown'),
                'author': doc.metadata.get('author', 'Unknown'),
            }
            doc.close()
            return metadata
        except Exception as e:
            print(f"Error extracting PDF metadata: {str(e)}", file=sys.stderr)
            return {'page_count': 0, 'title': 'Unknown', 'author': 'Unknown'}
            