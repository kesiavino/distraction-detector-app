# Distraction Detector App

*** forked from [horaja/distraction-detector-app](https://github.com/horaja/distraction-detector-app).  
> Contributions by Kesia Ann Vino: Team leader - working on the development of the AI algorithm, focusing on building a learning model capable of adapting to user-specific expressions such as frustration and confusion over time through continuous feedback and expression tracking.

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
2.5 Activate venv python interpreter in vscode
	 cmd+shift+p
	 Type Python: Select Interpreter
	 select enter interpreter path
	 go into your terminal, do cd .venv/bin/ and then type pwd to get the full working directory path
	 copy that and paste while augmenting "/python" at the end
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
