AI Basketball Shot Coach

![alt text](https://img.shields.io/badge/python-3.9+-blue.svg)


![alt text](https://img.shields.io/badge/FastAPI-0.78.0-blueviolet)


![alt text](https://img.shields.io/badge/License-MIT-yellow.svg)

An AI-powered application designed to analyze basketball shooting form from a video. This tool uses computer vision and pose estimation to provide detailed, actionable feedback, helping players improve their technique. It breaks down the shot into four key stages and compares the player's form to an exemplary model.
Features

    Video Analysis: Upload a video of your basketball shot for a complete form analysis.

    Pose Estimation: Utilizes MediaPipe to accurately detect 33 body landmarks and calculate joint angles.

    Four-Stage Breakdown: Analyzes the shot across four distinct phases: "Loading," "Gather," "Release," and "Follow-through."

    Quantitative Feedback: Calculates the deviation of key joint angles from an exemplary model.

    Qualitative Corrections: Provides specific, easy-to-understand feedback on what to improve for each stage of the shot.

    Key Frame Identification: Automatically identifies and returns the most representative frame for each of the four shooting stages.

    RESTful API: A clean and simple API for easy integration with frontend applications.

How It Works

The application follows a sophisticated pipeline to analyze a user's shot:

    Video Upload: The user sends a video file to the backend API.

    Frame Extraction: The system processes the video, extracting frames at a set interval.

    Pose Landmark Detection: Each frame is analyzed by MediaPipe Pose to identify the coordinates of the player's body landmarks.

    Angle Calculation: The system calculates 10 key joint angles (elbows, wrists, shoulders, hips, and knees) from the landmark data.

    Similarity Scoring: Each frame's calculated angles are compared against pre-defined JSON files representing the "perfect" form for each of the four shooting stages. A similarity score is computed to find the best match.

    Key Frame Selection: The frames with the highest similarity score for "Loading," "Gather," "Release," and "Follow-through" are selected as the key frames, ensuring they are in the correct temporal order.

    Feedback Generation: The angle differences between the user's key frames and the exemplary data are calculated. This data is used to generate personalized feedback and correction tips based on a weighted scoring system.

    API Response: The final analysis, including the percentage score for each stage, detailed feedback, and the key frames (encoded in base64), is returned as a JSON response.

Technologies Used

    Backend: FastAPI, Uvicorn

    Computer Vision: OpenCV, MediaPipe

    Data Handling: NumPy

Project Structure
code Code

    
.
├── data/
│   ├── exemplary_data/      # Stores JSON files with ideal joint angles for each shot stage.
│   └── user_shots/          # Default directory for user-uploaded videos.
├── routers/
│   └── api.py               # Defines the main API endpoints (e.g., for file upload).
├── utils/
│   ├── api_additional.py    # Helper functions for cleaning directories and encoding frames.
│   ├── feedback.py          # Generates qualitative feedback based on angle differences.
│   ├── film_scanner.py      # Core logic for video processing, analysis, and feedback orchestration.
│   ├── scan_ex_data.py      # Utility script to create exemplary data from images.
│   ├── scanner.py           # Scans images/frames to detect landmarks and calculate angles.
│   └── similarity.py        # Compares user's form to exemplary data to find best-matching frames.
├── main.py                  # Main FastAPI application entry point.
├── test.py                  # Script for testing the film scanning functionality.
└── requirements.txt         # Project dependencies.

  

Installation and Setup

    Clone the repository:
    code Bash

    
git clone https://github.com/your-username/ai-basketball-coach.git
cd ai-basketball-coach

  

Create and activate a Python virtual environment:
code Bash

    
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

  

Install the required dependencies:
code Bash

        
    pip install -r requirements.txt

      

    (Note: A requirements.txt file would need to be created containing dependencies like fastapi, uvicorn, opencv-python, mediapipe, and numpy)

    Generate Exemplary Data (First-time setup):
    To analyze shots, the system needs reference data.

        Place your ideal form images (named loading.jpg, gather.jpg, release.jpg, follow.jpg) in a temporary folder.

        Run the scan_ex_data.py script to generate the required JSON files in the data/exemplary_data/ directory.

Usage

    Run the FastAPI server:
    code Bash

    
fastapi dev main.py

  

The API will be available at http://127.0.0.1:8000.

Access the API Documentation:
Interactive API documentation (Swagger UI) is available at http://127.0.0.1:8000/docs.

Send a Video for Analysis:
Use a tool like curl or Postman to send a POST request to the /analyze/ endpoint with a video file.

Example using curl:
code Bash

        
    curl -X POST -F "file=@/path/to/your/shot_video.mp4" http://127.0.0.1:8000/analyze/

      

    Expected Response:
    The API will return a JSON object containing the detailed feedback and base64-encoded key frames for each of the four shot stages.

Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and create a pull request. You can also open an issue with the "enhancement" tag to propose new features.

    Fork the Project.

    Create your Feature Branch (git checkout -b feature/AmazingFeature).

    Commit your Changes (git commit -m 'Add some AmazingFeature').

    Push to the Branch (git push origin feature/AmazingFeature).

    Open a Pull Request.

License

This project is distributed under the MIT License. See LICENSE for more information.
