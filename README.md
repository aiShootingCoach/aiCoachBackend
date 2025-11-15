## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/ai-basketball-coach.git
    cd ai-basketball-coach
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    *(Note: A `requirements.txt` file would need to be created containing dependencies like `fastapi`, `uvicorn`, `opencv-python`, `mediapipe`, and `numpy`)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Generate Exemplary Data (First-time setup):**
    To analyze shots, the system needs reference data.
    -   Place your ideal form images (named `loading.jpg`, `gather.jpg`, `release.jpg`, `follow.jpg`) in a temporary folder.
    -   Run the `scan_ex_data.py` script to generate the required JSON files in the `data/exemplary_data/` directory.

## Usage

1.  **Run the FastAPI server:**
    ```bash
    fastapi dev main.py
    ```
    The API will be available at `http://127.0.0.1:8000`.

2.  **Access the API Documentation:**
    Interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.

3.  **Send a Video for Analysis:**
    Use a tool like `curl` or Postman to send a POST request to the `/uploadfile/` endpoint (or your defined upload endpoint) with a video file.

    **Example using `curl`:**
    ```bash
    curl -X POST -F "file=@/path/to/your/shot_video.mp4" http://127.0.0.1:8000/uploadfile/
    ```

    **Expected Response:**
    The API will return a JSON object containing the detailed feedback and base64-encoded key frames for each of the four shot stages.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and create a pull request. You can also open an issue with the "enhancement" tag to propose new features.

1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## License

This project is distributed under the MIT License. See `LICENSE` for more information.
