# Audio/Video Transcription App

This application uses OpenAI's Whisper model to transcribe audio and video files.

## Features

- Supports MP3, MP4, WAV, and M4A file formats
- Automatically splits large files for processing
- Provides a simple web interface using Gradio

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/transcription-app.git
   cd transcription-app
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the application:
```
python transcript.py
```

Then open a web browser and go to the URL displayed in the console (usually http://localhost:7860).

## Notes

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

