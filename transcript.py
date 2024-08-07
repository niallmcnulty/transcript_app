import gradio as gr
from openai import OpenAI
import os
from pathlib import Path
import tempfile
from pydub import AudioSegment
import math

# Initialize the OpenAI client with the API key
client = OpenAI(api_key="sk-proj-EWbPEfraqjjut0SPA9dQT3BlbkFJI6iTytfBUZdodPytNzKH")

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB in bytes
CHUNK_SIZE = 24 * 1024 * 1024  # 24 MB in bytes for safety margin

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

def transcribe_file(file):
    if file is None:
        return "Please upload a file.", None
    
    file_path = Path(file.name)
    
    if file_path.suffix.lower() not in ['.mp3', '.mp4']:
        return "Please upload an MP3 or MP4 file.", None
    
    if file_path.stat().st_size > MAX_FILE_SIZE:
        chunks = split_audio(file_path, CHUNK_SIZE)
        full_transcript = ""
        
        for chunk in chunks:
            with open(chunk, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            full_transcript += transcript.text + " "
            os.unlink(chunk)  # Delete the temporary chunk file
        
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

# Create the Gradio interface
iface = gr.Interface(
    fn=transcribe_file,
    inputs=[
        gr.File(label="Upload MP3 or MP4 file")
    ],
    outputs=[
        gr.Textbox(label="Transcription"),
        gr.File(label="Download Transcript")
    ],
    title="Audio/Video Transcription App",
    description="Upload an MP3 or MP4 file to transcribe. Large files will be automatically split and processed.",
    allow_flagging="never",
)

# Launch the interface
iface.launch()
