# ReadPDFs

A Python client for the ReadPDFs API that allows you to process PDF files and images, converting them to markdown.

## Installation

```bash
pip install readpdfs
```

## Usage

### Basic Client Usage

```python
from readpdfs import ReadPDFs

# Initialize the client
client = ReadPDFs(api_key="your_api_key")

# Process a PDF from a URL
result = client.process_pdf(pdf_url="https://example.com/document.pdf")

# Process a local PDF file
result = client.process_pdf(file_path="path/to/local/document.pdf")

# Process PDF from file content
with open("document.pdf", "rb") as f:
    content = f.read()
    result = client.process_pdf(file_content=content, filename="document.pdf")

# Process an image from URL
result = client.process_image(image_url="https://example.com/image.jpg")

# Process a local image file
with open("image.jpg", "rb") as f:
    content = f.read()
    result = client.process_image(file_content=content, filename="image.jpg")

# Fetch markdown content
markdown = client.fetch_markdown(url="https://api.readpdfs.com/documents/123/markdown")

# Get user documents
documents = client.get_user_documents(clerk_id="user_123")
```

### FastAPI Integration

```python
from fastapi import FastAPI, File, UploadFile, HTTPException
from readpdfs import ReadPDFs
from typing import Optional

app = FastAPI()
client = ReadPDFs(api_key="your_api_key")

@app.post("/process-pdf")
async def process_pdf(
    pdf_url: Optional[str] = None,
    file: Optional[UploadFile] = File(None),
    quality: str = "standard"
):
    try:
        if pdf_url and file:
            raise HTTPException(
                status_code=400,
                detail="Provide either pdf_url or file, not both"
            )
            
        if pdf_url:
            result = client.process_pdf(pdf_url=pdf_url, quality=quality)
        elif file:
            content = await file.read()
            result = client.process_pdf(
                file_content=content,
                filename=file.filename,
                quality=quality
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Either pdf_url or file must be provided"
            )
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-image")
async def process_image(
    image_url: Optional[str] = None,
    file: Optional[UploadFile] = File(None),
    quality: str = "standard"
):
    try:
        if image_url and file:
            raise HTTPException(
                status_code=400,
                detail="Provide either image_url or file, not both"
            )
            
        if image_url:
            result = client.process_image(image_url=image_url, quality=quality)
        elif file:
            content = await file.read()
            result = client.process_image(
                file_content=content,
                filename=file.filename,
                quality=quality
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Either image_url or file must be provided"
            )
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Features

- Process PDFs from URLs, local files, or file content
- Process images from URLs or file content
- Convert PDFs and images to markdown
- Fetch markdown content
- Retrieve user documents
- Configurable processing quality
- FastAPI integration support

## Requirements

- Python 3.7+
- requests library

For FastAPI integration:
- fastapi
- python-multipart
- uvicorn

## API Examples

### cURL

```bash
# Process PDF from URL
curl -X POST "http://localhost:8000/process-pdf?pdf_url=https://example.com/document.pdf&quality=high"

# Upload PDF file
curl -X POST "http://localhost:8000/process-pdf?quality=high" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/local/document.pdf"

# Process image from URL
curl -X POST "http://localhost:8000/process-image?image_url=https://example.com/image.jpg&quality=high"

# Upload image file
curl -X POST "http://localhost:8000/process-image?quality=high" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/local/image.jpg"
```

### Python Requests

```python
import requests

# PDF URL method
response = requests.post(
    "http://localhost:8000/process-pdf",
    params={"pdf_url": "https://example.com/document.pdf", "quality": "high"}
)

# PDF file upload method
with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/process-pdf",
        params={"quality": "high"},
        files={"file": f}
    )

# Image URL method
response = requests.post(
    "http://localhost:8000/process-image",
    params={"image_url": "https://example.com/image.jpg", "quality": "high"}
)

# Image file upload method
with open("image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/process-image",
        params={"quality": "high"},
        files={"file": f}
    )

result = response.json()
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```

The main changes in this update:
1. Updated the introduction to mention image processing
2. Added image processing examples to the Basic Client Usage section
3. Added a new FastAPI endpoint for image processing
4. Updated the Features list to include image processing capabilities
5. Added image processing examples to both cURL and Python Requests sections
6. Maintained consistent structure throughout the documentation