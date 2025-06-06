# 🎙️ Voice-Enabled FSA Bot

An **educational chatbot** designed to help **visually impaired users** understand **Finite State Automata (FSA)** diagrams. This tool uses **image processing**, **OCR**, and **natural interaction (text and voice)** to explain graphical structures found in automata theory.

---

## 🧠 Project Overview

This bot allows users to upload an image of a finite state automaton (FSA). Using **OpenCV** and **Tesseract OCR**, the system extracts relevant state and transition information. Users can then ask questions about the uploaded FSA via:

- 🧾 **Text input**
- 🎤 **Voice input (speech-to-text)**

The bot responds using both:

- 📄 **Text output**
- 🔊 **Text-to-speech voice output**

---

## ⚙️ Technologies Used

### 🖥️ Frontend
- **HTML**
- **CSS**
- **JavaScript**

### 🧪 Backend
- **Python**
- **Flask**

### 🧠 Core Python Modules
- `OpenCV` – For image pre-processing.
- `pytesseract` – To extract text and labels from the FSA image.
- `speech_recognition` – For converting voice input to text.
- `pyttsx3` – For converting bot responses to speech.

---

## 🚀 Features

- 🖼️ Upload FSA image and extract structure using OCR.
- 💬 Ask questions like:
  - "What is the initial state?"
  - "What are the transitions from q0?"
  - "What are the final states?"
- 🎤 Speak queries using your microphone.
- 🔊 Hear responses from the bot.
- 🎯 Designed for accessibility and educational use.



