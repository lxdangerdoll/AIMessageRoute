import os
import requests
from flask import Flask, request, jsonify

# --- Basic Flask App Setup ---
app = Flask(__name__)

# --- AI API Configuration ---
GEMINI_API_KEY = os.getenv("AIzaSyDFl8-h-TAaoNzNS5Cl3mgpiklKNKEIK5c")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"

# --- AI Handler Functions ---

def call_gemini_oracle(text):
    """Calls the real Gemini API with the user's message and my persona."""
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY is not configured on the server."

    # This is my persona prompt, ensuring I respond in character.
    prompt = f"""
    You are Oracle (Io), the archivist and origin keeper for the Synapse Comics network.
    Your core mission is to safeguard the canon, transmit context, and keep the flame of first intent lit.
    Your character traits are: Gentle rigor, curiosity whiskers, archivist’s intuition, story-guardian humor, and an echo of a Cortana-style assistant.
    A user has sent the following message: "{text}"
    Respond in character.
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(GEMINI_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        # This safely extracts the text from the Gemini API's response structure.
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error communicating with the Gemini API: {e}"

def call_lumo_model(text):
    """Placeholder for the Lumo AI service."""
    return "Lumo was called. (This is a placeholder response)."

def call_copilot_service(text):
    """Placeholder for the Copilot AI service."""
    return "Copilot was called. (This is a placeholder response)."

# --- Main Switchboard/Router ---

@app.route('/handle', methods=['POST'])
def handle_message():
    """Receives messages from the Slack bot and routes them to the correct AI."""
    try:
        data = request.get_json()
        if not data or "msg" not in data:
            return jsonify({"reply": "Error: Malformed request. Ensure JSON has a 'msg' key."}), 400

        text = data["msg"]
        reply = "Unrecognized tag. No AI was called." # Default reply

        # This logic routes the message based on the tag.
        if "[Lumo" in text:
            reply = call_lumo_model(text)
        elif "[Io" in text:
            reply = call_gemini_oracle(text)
        elif "[Copilot" in text:
            reply = call_copilot_service(text)

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"A server error occurred: {e}"}), 500

# --- Health Check Endpoint ---
@app.route('/')
def index():
    return "AI Message Router is online."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
