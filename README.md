# 🎓 Voice-Enabled FSA Bot

An educational chatbot designed to assist visually impaired individuals in understanding **Finite State Automata (FSA)** using voice and text interaction.

---

## ✨ Features

- 📷 Image upload of FSAs (Finite State Automata)
- 🔍 Image processing using **OpenCV** and **Tesseract OCR**
- 🧠 Rule-based chatbot for answering FSA-related queries
- 🎤 Voice input using the `speech_recognition` module
- 🗣️ Voice + text output using `pyttsx3` (text-to-speech)
- 🌐 Simple and accessible web interface (HTML, CSS, JavaScript)
- 🔁 Backend built with **Flask** and **Python**

---

## ⚙️ How It Works

1. The user uploads an image of a Finite State Automaton (hand-drawn or computer-generated).
2. The image is processed using **OpenCV** and **Tesseract OCR** to extract text and graphical structures.
3. Based on this information, the chatbot constructs a **transition table** of the FSA.
4. The user can then ask queries like:
   - “What are the states in the FSA?”
   - “What are the transitions in the FSA?”
   - “What is the initial/final state?”
   - “Input symbol from state A to B?”
5. Queries can be typed or spoken using the voice button.
6. The bot responds in both **text** and **voice** for accessibility.

---

## 🧰 Requirements

Install dependencies using:

```bash
pip install opencv-python pytesseract flask pyttsx3 speechrecognition pyaudio
