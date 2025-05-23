# Write the code to:
# Access the webcam using OpenCV.
# Capture frames.
# Process frames with MediaPipe Face Mesh to get facial landmarks.
# (For now) Display the camera feed with landmarks drawn on it so you can see it's working.
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import time
from flask import Flask, jsonify
from flask_cors import CORS
import threading

# --- Global Variables ---
latest_landmarks = None
distraction_status_output = {"distracted": False}
# To ensure drawing and processing happen with consistent data
# (especially important due to the async nature of landmarker)
lock = threading.Lock()

# --- Step 1. Mediapipe setup ---
# Define the path to your downloaded model
MODEL_PATH = 'face_landmarker.task'

# Create a FaceLandmarker object.
BaseOptions = python.BaseOptions
FaceLandmarker = vision.FaceLandmarker
FaceLandmarkerOptions = vision.FaceLandmarkerOptions
VisionRunningMode = vision.RunningMode

# This function will be called when landmarks are detected
def result_callback(result: vision.FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
	global latest_landmarks
	with lock: # Ensure thread-safe updates
			if result.face_landmarks:
					latest_landmarks = result.face_landmarks
			else:
					latest_landmarks = None
	# Note: We'll do the drawing and main logic in the main loop to keep OpenCV happy,
	# using the 'latest_landmarks' variable.
    
options = FaceLandmarkerOptions(
	base_options=BaseOptions(model_asset_path=MODEL_PATH),
	running_mode=VisionRunningMode.LIVE_STREAM, # Important for webcam
	num_faces=1,
	min_face_detection_confidence=0.5,
	min_face_presence_confidence=0.5, # Helps ensure face is truly present
	min_tracking_confidence=0.5,
	output_face_blendshapes=False, # Not needed for this phase, can save computation
	output_facial_transformation_matrixes=False, # Not needed for this phase
	result_callback=result_callback # Our custom callback function
)

# The landmarker object will be created in the main loop function
landmarker = None

# --- Step 2: Placeholder (Non?-)ML Algorithm for determining distraction ---
def simple_distraction_logic(face_landmarks_detected_in_current_frame):
	"""
	Extremely simple placeholder logic.
	"""
	if face_landmarks_detected_in_current_frame:
			return False # Not distracted if face landmarks are present
	else:
			return True # Distracted if no face landmarks (e.g., turned away completely)
      
# --- Step 3: Basic Flask Server Setup ---
app = Flask(__name__)
CORS(app)

@app.route('/status', methods=['GET'])
def get_status():
	global distraction_status_output
	return jsonify(distraction_status_output)
  
def run_flask_app():
	print("Starting Flask server on http://localhost:5000")
	app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    
# --- Main Application Logic: Camera and MediaPipe Integration ---
def camera_and_detection_loop():
	global latest_landmarks, distraction_status_output, landmarker
	
	try:
		landmarker = FaceLandmarker.create_from_options(options)
	except Exception as e:
		print(f"Error creating FaceLandmarker: {e}")
		print(f"Ensure '{MODEL_PATH}' is in the correct location.")
		return

	cap = cv2.VideoCapture(0);
	if not cap.isOpened():
		print('Error: Cannot open webcam.')
		if landmarker:
			landmarker.close()
		return
	
	frame_timestamp_ms = 0
	print("Starting camera feed and landmark detection using MediaPipe Tasks...")
	while cap.isOpened():
		success, frame = cap.read()
		if not success:
			print('Ignoring empty camera frame.')
			continue

		frame = cv2.flip(frame, 1)
		rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  
		mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
  
		frame_timestamp_ms = int(time.time() * 1000)
  
		landmarker.detect_async(mp_image, frame_timestamp_ms)

		display_landmarks = None
		face_currently_detected = False
		with lock:
			if latest_landmarks:
				display_landmarks = latest_landmarks
				face_currently_detected = True
    
		current_distraction_state = simple_distraction_logic(face_currently_detected)
		distraction_status_output["distracted"] = current_distraction_state
  
		if cv2.waitKey(5) & 0xFF == 27: # ESC to exit
			break
	cap.release()
	cv2.destroyAllWindows()
	if landmarker:
		landmarker.close()
	
	print('Camera and detection loop successfully stopped')
  

if __name__ == "__main__":
  flask_thread = threading.Thread(target=run_flask_app, daemon=True)
  flask_thread.start()
  
  camera_and_detection_loop()
  print("Application Exiting.")