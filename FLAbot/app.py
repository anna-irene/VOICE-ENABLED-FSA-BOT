from flask import Flask, render_template, request, jsonify
import os
from fsa_processor import process_fsa_image
from chatbot import FSAChatbot

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")
    fsa_data = data.get("fsa_data")
    voice_input = data.get("voice_input", False)
    
    if not fsa_data:
        return jsonify({"error": "Invalid request - missing FSA data"}), 400
    
    print("Received FSA data:", fsa_data)
    
    try:
        # Initialize the chatbot with the FSA data
        chatbot = FSAChatbot(fsa_data)
        
        # Handle voice input
        if voice_input:
            question = chatbot.listen()
            if not question:
                return jsonify({"response": "No question detected. Please try again."})
        
        # If no question provided (for voice input case)
        if not question:
            return jsonify({"response": "No question detected. Please try again."})
        
        # Get the response from the chatbot
        response = chatbot.answer_question(question)
        
        # Clean up resources
        del chatbot
        
        print("Chatbot response:", response)
        return jsonify({
            "response": response, 
            "question": question if question else "Voice question"
        })
    except Exception as e:
        print("Error in chatbot:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/process_image", methods=["POST"])
def process_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only PNG and JPG are allowed."}), 400
    
    # Save the uploaded file
    upload_folder = "static"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    image_path = os.path.join(upload_folder, "uploaded_image.png")
    file.save(image_path)
    
    # Verify the file was saved
    if not os.path.exists(image_path):
        return jsonify({"error": "Failed to save the uploaded image"}), 500
    
    # Process the FSA image
    try:
        fsa_data = process_fsa_image(image_path)
        return jsonify({"success": True, "fsa_data": fsa_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========================== Main Function ==========================

if __name__ == "__main__":
    app.run(debug=True)
