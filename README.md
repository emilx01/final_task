Final Task Project
A Django-based API for cloud image processing. Upload files via a file picker or JSON, apply transformations, and get a temporary link to view results.
✨ Features
 1. Cloud Processing: Process and save images directly in the cloud.
 2. Flexible Uploads: Supports Multipart/form-data (file picker) or Base64 JSON inputs.
 3. Status Tracking: Check the real-time status of asynchronous image tasks.
 4. Secure Access: Generates temporary pre-signed links for viewing.
⚙️ Available Operations
 1. Geometry: Resizing, rotating, cropping, and adding padding.
 2. Color: Grayscale and RGB/BGR conversion.
 3. Format: PNG/JPG conversion and GIF creation from multiple images.
🚀 API Usage
1. Upload & Process
Endpoint: POST /api/upload/
Payload Example:
[{"type": "resize", "width": 1920, "height": 1080}, {"type": "rgb_bgr_conversion"}, {"type": "grayscale"}]
[{"type": "rotate", "angle": 90}]

2. Check Task Status
Endpoint: GET /api/requests/<request_id>/
Response:
{
  "task_id": "12345",
  "status": "SUCCESS",
  "input_file": "https://storage.googleapis.com/temp-link-to-image",
  "output_file": "https://storage.googleapis.com/temp-link-to-image"
}

🛠 Tech Stack
 1. Language: Python & Django
 2. Environment: Docker & Docker Compose
 3. Package Manager: uv
 4. Database: PostgreSQL
📂 Project Structure

```text
.
├── finaltask/            # Core Django configuration and settings
├── images/               # Directory for media assets and image processing
├── app.py                # Application entry point or utility script
├── manage.py             # Django command-line utility
├── Dockerfile            # Instructions for building the application image
├── docker-compose.yaml   # Service orchestration configuration
├── pyproject.toml        # Project metadata and dependencies
└── uv.lock               # Exact dependency versions for reproducible builds

```

🚥 Getting Started
Docker
 1. git clone https://github.com/emilx01/final_task.git
 2. cd final_task
 3. docker-compose up --build
Local
 1. uv sync
 2. python manage.py migrate
 3. python manage.py runserver