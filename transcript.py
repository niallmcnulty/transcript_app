import gradio as gr
from openai import OpenAI
import os
from pathlib import Path
import tempfile
from pydub import AudioSegment
import math
import logging
import atexit

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the OpenAI client with the API key from environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB in bytes
CHUNK_SIZE = 24 * 1024 * 1024  # 24 MB in bytes for safety margin
ALLOWED_EXTENSIONS = {'.mp3', '.mp4', '.wav', '.m4a'}

def split_audio(file_path, chunk_size):
    audio = AudioSegment.from_file(file_path)
    duration = len(audio)
    chunk_duration = math.ceil((chunk_size / len(audio.raw_data)) * duration)
    chunks = []
    
    for i in range(0, duration, chunk_duration):
        chunk = audio[i:i+chunk_duration]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_path.suffix) as temp_file:
            chunk.export(temp_file.name, format=file_path.suffix[1:])
            chunks.append(temp_file.name)
    
    return chunks

def cleanup_temp_files():
    temp_dir = tempfile.gettempdir()
    for file in os.listdir(temp_dir):
        if file.endswith('.mp3') or file.endswith('.mp4') or file.endswith('.wav') or file.endswith('.m4a') or file.endswith('.txt'):
            os.remove(os.path.join(temp_dir, file))

atexit.register(cleanup_temp_files)

def transcribe_file(file):
    try:
        if file is None:
            return "Please upload a file.", None
        
        file_path = Path(file.name)
        logger.info(f"Processing file: {file_path}")
        
        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            return f"Please upload a file with one of these extensions: {', '.join(ALLOWED_EXTENSIONS)}", None
        
        if file_path.stat().st_size > MAX_FILE_SIZE:
            chunks = split_audio(file_path, CHUNK_SIZE)
            full_transcript = ""
            
            for i, chunk in enumerate(chunks, 1):
                with open(chunk, "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file
                    )
                full_transcript += transcript.text + " "
                os.unlink(chunk)  # Delete the temporary chunk file
                yield f"Processed chunk {i}/{len(chunks)}", None
            
            # Save full transcript to a temporary file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
                temp_file.write(full_transcript)
            
            return full_transcript, temp_file.name
        else:
            # Original transcription logic for files under 25 MB
            with open(file_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
                temp_file.write(transcript.text)
            
            return transcript.text, temp_file.name
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}", None

# Create the Gradio interface
iface = gr.Interface(
    fn=transcribe_file,
    inputs=[
        gr.File(label="Upload audio file")
    ],
    outputs=[
        gr.Textbox(label="Transcription"),
        gr.File(label="Download Transcript")
    ],
    title="Audio/Video Transcription App",
    description="Upload an audio file (MP3, MP4, WAV, or M4A) to transcribe. Large files will be automatically split and processed.",
    allow_flagging="never",
)

# Launch the interface
if __name__ == "__main__":
    iface.launch()
