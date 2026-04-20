# Mini Robot

A personal robotics project to build a small assistant robot with a Jetson Orin Nano as the high-level brain and a microcontroller for real-time motor control.

## Current scope
- Voice input
- Speech-to-text
- Command parsing
- Simulated robot state
- Future motor control through MCU serial communication

## Goal
Build toward a small assistant robot and later a desk-scale biped demonstrator.

## Tech stack
- Python
- Jetson Orin Nano
- Vosk
- pyttsx3
- ESP32 (planned)

## Setup

Download the Vosk model manually:

https://alphacephei.com/vosk/models

Extract into:
voice/models/

Example:
voice/models/vosk-model-small-en-us-0.15