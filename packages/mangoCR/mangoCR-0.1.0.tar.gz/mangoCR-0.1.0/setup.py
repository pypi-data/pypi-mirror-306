from setuptools import setup, find_packages

setup(
    name="mangoCR",
    version="0.1.0",
    author="Sandeep Junnarkar",
    author_email="sjnews@gmail.com",
    description="A package to convert PDFs to images and perform OCR.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sandeepmj/mangoCR",
    packages=find_packages(),
    install_requires=[
        "pymupdf",
        "pytesseract",
        "Pillow",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
