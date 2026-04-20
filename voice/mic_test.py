import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path

SAMPLE_RATE = 16000
DURATION = 5 # seconds
OUTPUT_FILE = Path("voice") / "test_recording.wav"

def main():
    print("Recording will start now for 5 seconds...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    sd.wait()
    write(OUTPUT_FILE, SAMPLE_RATE, audio)
    print(f"Saved recording to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()