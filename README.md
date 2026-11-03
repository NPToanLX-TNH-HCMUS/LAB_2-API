# LAB 2 - Application Programming Interface

## Student Information

| Field | Detail |
| :--- | :--- |
| **Student ID** | 25127522 |
| **Student Name** | Ngo Phuoc Toan |
| **Email** | nptoan2527@clc.fitus.edu.vn |

---

## Model Information

- **Model Name:** `Baghdad99/saad-speech-recognition-hausa-audio-to-text`
- **Hugging Face Model Page:** [https://huggingface.co/Baghdad99/saad-speech-recognition-hausa-audio-to-text](https://huggingface.co/Baghdad99/saad-speech-recognition-hausa-audio-to-text)
- **Task:** Automatic Speech Recognition (ASR)
- **Language:** Hausa (`ha`)

---

## System Overview & Functionality

This project provides a API service for Automatic Speech Recognition (ASR) tailored to the Hausa language. The system wraps a pre-trained Hugging Face speech-to-text model into a high-performance backend using **FastAPI** and **Transformers**.

### Key Features:
- **Audio Transcription (`POST /predict`):** Accepts audio files (e.g., `.wav`), runs inference through Hugging Face's `automatic-speech-recognition` pipeline, and returns the transcribed text in JSON format.
- **Service Health Check (`GET /health`):** Verifies the server operational status and confirms whether the underlying ASR model pipeline is loaded and ready.
- **API Overview & Metadata (`GET /`):** Returns introductory metadata and a summary of available endpoints.
- **Automated Client Validation:** Includes an automated test suite (`src/client.py`) that executes test requests across all endpoints using sample audio files.

---

## Codebase Structure

```text
LAB_2-API/
├── src/
│   ├── __init__.py
│   ├── server.py              # FastAPI server application and endpoint handlers
│   └── client.py              # test and validate endpoints via requests library
├── tests/
│   └── test_files/
│       ├── test_1.wav         # Sample audio file 1
│       └── test_2.wav         # Sample udio file 2
├── pyproject.toml             # Project metadata, dependencies, and CLI script entry points
└──  README.md                  # Project documentation and usage guide
```

---

## Installation & Setup

### Prerequisites
- **Python**: Version `3.10` or higher

### 1. Clone or Open the Repository
```bash
cd LAB_2-API
```

### 2. Create and Activate a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**On Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

You can install the package and all required dependencies directly via `pip`:

```bash
pip install --upgrade pip
pip install -e .
```

## Running the Application

### 1. Start the Server

Once installed in editable mode, you can start the server using the configured console script:

```bash
server
```

The server will be available at: `http://localhost:8080`
- **Interactive Swagger Documentation:** [http://localhost:8080/docs](http://localhost:8080/docs)
- **ReDoc Documentation:** [http://localhost:8080/redoc](http://localhost:8080/redoc)

### 2. Run the Automated Client Tests

With the server running in one terminal, open another terminal (with the virtual environment activated) and run:

```bash
client
```
The client will test `GET /`, `GET /health`, `POST /predict` with sample files in `tests/test_files/`, and error validation (`POST /predict` with no file).

---

## API Usage & Endpoints

### 1. Introduction Endpoint

- **Endpoint:** `GET /`
- **Description:** Returns basic information about the API and available endpoints.

#### Example Request:
```bash
curl -X GET "http://localhost:8080/"
```

#### Example Response (`200 OK`):
```json
{
  "name": "Hausa Automatic Speech Recognition API",
  "description": "This API transcribes Hausa audio files into text using the Baghdad99/saad-speech-recognition-hausa-audio-to-text model from Hugging Face.",
  "endpoints": {
    "GET  /": "API introduction (this response)",
    "GET  /health": "Health check – reports whether the model is loaded and ready",
    "POST /predict": "Upload a WAV/audio file and receive its transcription as JSON"
  }
}
```

---

### 2. Health Check Endpoint

- **Endpoint:** `GET /health`
- **Description:** Verifies service readiness and model availability.

#### Example Request:
```bash
curl -X GET "http://localhost:8080/health"
```

#### Example Response (`200 OK`):
```json
{
  "status": "ok",
  "model": "Baghdad99/saad-speech-recognition-hausa-audio-to-text",
  "pipeline_ready": true
}
```

---

### 3. Speech-to-Text Prediction Endpoint

- **Endpoint:** `POST /predict`
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `file`: The audio file to be transcribed (`.wav` recommended).

#### Example Request using cURL:
```bash
curl -X POST "http://localhost:8080/predict" \
  -F "file=@tests/test_files/test_1.wav"
```

#### Example Request using Python (`requests`):
```python
import requests

url = "http://localhost:8080/predict"
file_path = "tests/test_files/test_1.wav"

with open(file_path, "rb") as f:
    files = {"file": (file_path, f, "audio/wav")}
    response = requests.post(url, files=files)

print(response.status_code)
print(response.json())
```

#### Example Response (`200 OK`):
```json
{
  "filename": "test_1.wav",
  "transcription": "bayan haka ya bayyana cewa"
}
```

#### Example Error Response (`422 Unprocessable Entity` - when no file is uploaded):
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "file"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

---

## Demonstration Video

- **Video Link:** [Link to Demonstration Video]()
