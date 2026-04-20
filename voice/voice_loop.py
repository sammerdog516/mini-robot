import json
import wave
from pathlib import Path

import sounddevice as sd
from scipy.io.wavfile import write
from vosk import Model, KaldiRecognizer

from voice.tts import speak
from sim.state import state
from control.serial_interface import send_to_mcu

SAMPLE_RATE = 16000
DURATION = 5
AUDIO_FILE = Path("voice") / "test_recording.wav"
MODEL_PATH = Path("voice") / "models" / "vosk-model-small-en-us-0.15"

def record_audio():
    print("Recording for 5 seconds...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    sd.wait()
    write(AUDIO_FILE, SAMPLE_RATE, audio)
    print(f"Saved recording to {AUDIO_FILE}")

def transcribe_audio():
    wf = wave.open(str(AUDIO_FILE), "rb")

    if wf.getnchannels() != 1:
        raise ValueError("Audio file must be mono.")
    if wf.getframerate() != 16000:
        raise ValueError("Audio file must be 16000 Hz.")
    
    model = Model(str(MODEL_PATH))
    recognizer = KaldiRecognizer(model, wf.getframerate())

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        recognizer.AcceptWaveform(data)

    result = json.loads(recognizer.FinalResult())
    return result.get("text", "")

def handle_command(text):
    text = text.lower().strip()
    previous_command = state["last_command"]
    state["last_command"] = text

    responses = []

    if "hello" in text:
        responses.append("Hello Sam")

    if "status" in text:
        responses.append(
            f"System {state['system_status']}. "
            f"Head angle is {state['head_angle']} degrees. "
            f"Arm angle is {state['arm_angle']} degrees."
        )
    
    if "last command" in text:
        if state["last_command"]:
            responses.append(f"Your last command was {previous_command}")
        else:
            responses.append("No command has been recorded yet.")
    if "head left" in text:
        state["head_angle"] -= 10
        responses.append(f"Head angle now {state['head_angle']} degrees")

    if "head right" in text:
        state["head_angle"] += 10
        responses.append(f"Head angle now {state['head_angle']} degrees")

    if "arm up" in text:
        state["arm_angle"] += 10
        responses.append(f"Arm angle now {state['arm_angle']} degrees")

    if "arm down" in text:
        state["arm_angle"] -= 10
        responses.append(f"Arm angle now {state['arm_angle']} degrees")

    if "center head" in text:
        state["head_angle"] = 0
        responses.append("Head centered")

    if "reset" in text:
        state["head_angle"] = 0
        state["arm_angle"] = 0
        responses.append("State reset")
    
    if not text:
        responses.append("I did not catch that.")
    elif not responses:
        responses.append(text)

    return " ".join(responses)


def main():
    record_audio()
    text = transcribe_audio()
    print("Transcription:", text)
    response = handle_command(text)
    speak(response)

if __name__ == "__main__":
    main()