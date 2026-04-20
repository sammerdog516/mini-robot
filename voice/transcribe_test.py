import json
import wave
from pathlib import Path
from tts import speak

from vosk import Model, KaldiRecognizer

AUDIO_FILE = Path("voice") / "test_recording.wav"
MODEL_PATH = Path("voice") / "models" / "vosk-model-small-en-us-0.15"

def main():
    if not AUDIO_FILE.exists():
        print(f"Audiio file not found: {AUDIO_FILE}")
        return
    
    if not MODEL_PATH.exists():
        print(f"Model path not found: {MODEL_PATH}")
        return
    
    wf = wave.open(str(AUDIO_FILE), "rb")

    if wf.getnchannels() != 1:
        print("Audio must be mono.")
        return
    
    if wf.getframerate() != 16000:
        print("Audio must 16000 Hz.")
        return
    
    model = Model(str(MODEL_PATH))
    recognizer = KaldiRecognizer(model, wf.getframerate())

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        recognizer.AcceptWaveform(data)

    result = json.loads(recognizer.FinalResult())
    print("Transcription:", result.get("text", ""))

    text = result.get("text", "")
    
    if text:
        speak(f"You said: {text}")
    else:
        speak("I did not catch that.")

if __name__ == "__main__":
    main()