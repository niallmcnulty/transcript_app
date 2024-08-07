# Audio Transcription App

This application provides a simple web interface for transcribing audio files (MP3 or MP4) using OpenAI's Whisper model. It supports file upload, automatic transcription, and transcript download.

## Features

- Upload MP3 or MP4 audio files
- Automatic transcription using OpenAI's Whisper model
- Support for large files (>25MB) through automatic file splitting
- Download transcripts as text files
- Simple and intuitive web interface

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- An OpenAI API key
- FFmpeg installed on your system (required for pydub to handle audio files)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/audio-transcription-app.git
   cd audio-transcription-app
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - On macOS (using Homebrew):
     ```
     brew install ffmpeg
     ```
   - On Ubuntu or Debian:
     ```
     sudo apt-get update
     sudo apt-get install ffmpeg
     ```
   - For other operating systems, please refer to the official FFmpeg documentation.

## Configuration

1. Open the `transcript.py` file.
2. Replace `"your-api-key-here"` with your actual OpenAI API key:
   ```python
   client = OpenAI(api_key="your-api-key-here")
   ```

## Usage

1. Run the application:
   ```
   python transcript.py
   ```

2. Open your web browser and go to the URL displayed in the console (typically http://127.0.0.1:7860).

3. Use the interface to upload an MP3 or MP4 file.

4. Wait for the transcription to complete.

5. View the transcription in the interface and download the transcript file if desired.

## Notes

- The application automatically splits files larger than 25MB into smaller chunks for processing.
- Transcription of very large files may take some time and use multiple API calls.
- Ensure your OpenAI account has sufficient credits for transcription tasks.

## Troubleshooting

- If you encounter issues with file processing, ensure FFmpeg is correctly installed and accessible in your system PATH.
- For API-related errors, check that your OpenAI API key is correct and has the necessary permissions.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the Whisper transcription model
- Gradio for the easy-to-use web interface framework
- Pydub for audio file handling

