# MangoCR

![Turn obnoxious PDFs into a tasty mango slices!](https://sandeepmj.github.io/image-host/mangoCR-graphic.png)

*Turn obnoxious PDFs into a tasty mango slices!*

MangoCR is a Python package that converts PDF files to text using Optical Character Recognition (OCR). It processes single or multiple PDF files and outputs the results in a clean Markdown format.

## Features

- Process single or multiple PDF files in one go
- High-quality OCR using Tesseract
- Markdown-formatted output
- Progress tracking for each PDF and page
- Maintains document structure with clear page separation
- High-resolution image conversion (300 DPI) for optimal OCR results

## Prerequisites

- Python 3.6 or higher
- Tesseract OCR engine

## Installation

1. Clone the repository and install the required Python packages:

```bash
pip install mangoCR
```

2. Install Tesseract OCR engine:

### Windows
1. Download the Tesseract installer from the [official GitHub releases page](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer. Make sure to note the installation path
3. Add Tesseract to your system PATH:
   - Open System Properties → Advanced → Environment Variables
   - Under System Variables, find and select "Path"
   - Click "Edit" and add the Tesseract installation directory (typically `C:\Program Files\Tesseract-OCR`)
   - Click "OK" to save

### macOS
Using Homebrew:
```bash
brew install tesseract
```

### Google Colab
```bash
!apt install tesseract-ocr
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### Linux (Fedora)
```bash
sudo dnf install tesseract
```

## Usage

The package provides a simple function `pdf2image_ocr` that can process either a single PDF or multiple PDFs.

### Basic Usage

```python
from mangoCR import pdf2image_ocr

# Process a single PDF
pdf2image_ocr("path/to/your/document.pdf")

# Process multiple PDFs
pdf_list = [
    "path/to/first.pdf",
    "path/to/second.pdf",
    "path/to/third.pdf"
]
pdf2image_ocr(pdf_list)
```

### Specifying Custom Output File

```python
# Change the output file name/location
pdf2image_ocr("document.pdf", output_file="custom_output.md")
```

## Output Format

The OCR results are saved in a Markdown file with the following structure:

```markdown
# OCR Results for document1.pdf

## Page 1

[Extracted text from page 1]

## Page 2

[Extracted text from page 2]

# OCR Results for document2.pdf

## Page 1

[Extracted text from page 1]
```

## Troubleshooting

### Common Issues

1. **Tesseract Not Found Error**
   ```
   EnvironmentError: Tesseract is not installed or not found in PATH
   ```
   Solution: Ensure Tesseract is properly installed and added to your system PATH.

2. **Low Quality OCR Results**
   - Ensure your PDF is of good quality
   - The default DPI is set to 300 for optimal results
   - Consider preprocessing your PDFs if they contain complicated layouts

### PDF Requirements

- PDFs should be readable and not password-protected
- Scanned documents should be clear and properly aligned
- For best results, use PDFs with a resolution of at least 300 DPI

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Tesseract OCR team for providing the OCR engine
- PyMuPDF team for the excellent PDF processing library
