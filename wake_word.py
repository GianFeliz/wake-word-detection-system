import vosk
import json
import time
from rapidfuzz import fuzz
import pyaudio

# === CONFIGURATION ===
WAKE_PHRASE = ["hello", "nova"]  # Two-word wake phrase — modify to change wake word
FUZZY_THRESHOLD = 80             # Similarity threshold (0-100). Lower = more lenient, Higher = stricter
MODEL_PATH = "model"             # Path to Vosk model folder. Download from: https://alphacephei.com/vosk/models
                                 # Recommended: vosk-model-small-en-us-0.15 for English
MIC_DEVICE_INDEX = 15            # Microphone device index. Run list_audio_devices() below to find yours
SAMPLE_RATE = 16000              # Sample rate in Hz. Must match the Vosk model's expected rate
CHUNK_SIZE = 4000                # Number of audio frames per read. Adjust if experiencing latency

# === HELPER: List available audio input devices ===
# Uncomment and run this block once to find your MIC_DEVICE_INDEX
# def list_audio_devices():
#     p = pyaudio.PyAudio()
#     print("Available audio input devices:")
#     for i in range(p.get_device_count()):
#         info = p.get_device_info_by_index(i)
#         if info['maxInputChannels'] > 0:
#             print(f"  Index {i}: {info['name']}")
#     p.terminate()
# list_audio_devices()

# === Load Vosk Model ===
# Ensure the model folder exists at MODEL_PATH before running
model = vosk.Model(MODEL_PATH)
rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)

def match_wake_phrase(text):
    """
    Checks if the transcribed text contains the wake phrase using fuzzy matching.
    Searches all consecutive word pairs (bigrams) in the transcribed text.
    Also handles cases where the ASR engine merges the wake phrase into one word.
    
    Args:
        text (str): Transcribed text from Vosk ASR
    Returns:
        bool: True if wake phrase detected, False otherwise
    """
    text = text.lower().strip()
    words = text.split()

    # Check all consecutive word pairs for fuzzy match against wake phrase
    for i in range(len(words) - 1):
        first_word = words[i]
        second_word = words[i + 1]

        score_first = fuzz.ratio(first_word, WAKE_PHRASE[0])
        score_second = fuzz.ratio(second_word, WAKE_PHRASE[1])

        if score_first >= FUZZY_THRESHOLD and score_second >= FUZZY_THRESHOLD:
            return True

    # Fallback: check merged phrase in case ASR combines the two words
    merged_text = text.replace(" ", "")
    merged_phrase = "".join(WAKE_PHRASE)
    if fuzz.partial_ratio(merged_text, merged_phrase) >= FUZZY_THRESHOLD:
        return True

    return False

# === Initialize PyAudio ===
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE,
                input_device_index=MIC_DEVICE_INDEX)

print("Listening to microphone input...")
print(f"Wake phrase: '{' '.join(WAKE_PHRASE)}'")
print(f"Fuzzy threshold: {FUZZY_THRESHOLD}")

# Tracks time elapsed from when listening begins
listen_start_time = time.time()

try:
    while True:
        data = stream.read(CHUNK_SIZE, exception_on_overflow=False)

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "").lower()

            if text and match_wake_phrase(text):
                elapsed = round(time.time() - listen_start_time, 2)
                print(f"Wake phrase detected at {elapsed} seconds.")
                break

finally:
    # Ensure audio stream is properly closed even if an error occurs
    stream.stop_stream()
    stream.close()
    p.terminate()

print("Finished processing.")