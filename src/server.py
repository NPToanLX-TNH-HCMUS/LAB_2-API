import os
import tempfile

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from transformers import pipeline

app = FastAPI(
    title="ASR API",
    description=(
        "A REST API that exposes the Baghdad99/saad-speech-recognition-hausa-audio-to-text "
        "Hugging Face model for automatic speech recognition (ASR)."
    ),
    version="0.1.0",
)

asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model="Baghdad99/saad-speech-recognition-hausa-audio-to-text",
    return_timestamps=True,
)


@app.get("/")
def introduce():
    """Return a brief description of the API and its available endpoints."""
    return {
        "name": "Hausa Automatic Speech Recognition API",
        "description": (
            "This API transcribes Hausa audio files into text using the "
            "Baghdad99/saad-speech-recognition-hausa-audio-to-text model from Hugging Face."
        ),
        "endpoints": {
            "GET  /": "API introduction (this response)",
            "GET  /health": "Health check – reports whether the model is loaded and ready",
            "POST /predict": "Upload a WAV/audio file and receive its transcription as JSON",
        },
    }


@app.get("/health")
def health():
    """Check whether the ASR model pipeline is loaded and the service is operational."""
    if asr_pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="ASR pipeline is not initialised – service unavailable.",
        )
    return {
        "status": "ok",
        "model": "Baghdad99/saad-speech-recognition-hausa-audio-to-text",
        "pipeline_ready": True,
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Receive an audio file (WAV recommended), run it through the ASR model,
    and return the transcription as JSON.

    - **file**: Audio file to transcribe (multipart/form-data).
    """
    suffix = os.path.splitext(file.filename)[-1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        result = asr_pipeline(tmp_path)
        transcription = result.get("text", "")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inference error: {exc}") from exc
    finally:
        os.remove(tmp_path)

    return JSONResponse(
        content={
            "filename": file.filename,
            "transcription": transcription,
        }
    )


def main():
    uvicorn.run("src.server:app", host="localhost", port=8080, reload=True)


if __name__ == "__main__":
    main()
