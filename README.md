# Wake Word Detection System

An offline wake word detection system using Vosk ASR 
and fuzzy string matching via RapidFuzz.

Developed during internship at Delta-NTU Corporate Laboratory as 
part of a modular audio-interactive surveillance robot system.

## How It Works
1. Audio is captured from the microphone in real time
2. Vosk transcribes the audio stream to text offline
3. RapidFuzz compares transcribed text against the wake phrase 
   using Levenshtein distance based fuzzy matching
4. Detection triggers when both words of the wake phrase 
   exceed the similarity threshold simultaneously

## Requirements
- Python 3.8+
- vosk
- pyaudio
- rapidfuzz

Install dependencies:
pip install vosk pyaudio rapidfuzz

## Setup

### 1. Download Vosk Model
Download a model from https://alphacephei.com/vosk/models

Recommended: vosk-model-small-en-us-0.15 for English

Extract and place the model folder in the same directory as 
the script. Update MODEL_PATH in the configuration if needed.

### 2. Find Your Microphone Device Index
Uncomment the list_audio_devices() block in the script and run 
it once to see available audio input devices and their indices.
Update MIC_DEVICE_INDEX accordingly.

## Configuration
| Parameter | Default | Description |
|-----------|---------|-------------|
| WAKE_PHRASE | ["hello", "nova"] | Two word wake phrase |
| FUZZY_THRESHOLD | 80 | Similarity threshold 0-100 |
| MODEL_PATH | "model" | Path to Vosk model folder |
| MIC_DEVICE_INDEX | 15 | Microphone device index |
| SAMPLE_RATE | 16000 | Audio sample rate in Hz |
| CHUNK_SIZE | 4000 | Audio frames per read |

## How to Run
python wake_word.py

## Acknowledgements
Developed at Delta-NTU Corporate Laboratory, 
Nanyang Technological University

## License
MIT License
