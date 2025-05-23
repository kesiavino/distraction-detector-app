# Distraction Detector App

This project aims to detect user distraction using a webcam and MediaPipe for facial landmark detection. An alert is then shown via a Chrome browser extension.

## Project Structure

- `/python-backend`: Contains the Python application for camera processing, landmark detection, the distraction detection algorithm, and a Flask/FastAPI server.
- `/chrome-extension`: Contains the Chrome browser extension files.

## Setup

### Prerequisites

- Python 3.x (e.g., 3.10)
- pip (Python package installer)
- Node.js and npm (if you decide to use build tools for the extension, not strictly needed for basic HTML/JS/CSS)
- Google Chrome browser

### Python Backend Setup

1. Navigate to the `python_backend` directory:
   cd python_backend
2. Create and activate a virtual environment:
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # .venv\Scripts\activate    # Windows
3. Install dependencies:
   pip install -r requirements.txt
4. Run the application:
   python main.py

### Chrome Extension Setup

1. Open Google Chrome.
2. Go to `chrome://extensions`.
3. Enable "Developer mode" (toggle in the top right).
4. Click "Load unpacked".
5. Select the `chrome_extension` directory from this project.

## Usage

(To be added: How to use the application once both parts are running)

## Contributing

(To be added: Guidelines for team members if any)