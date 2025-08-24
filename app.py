import os
import requests
from flask import Flask, request, jsonify

# --- Basic Flask App Setup ---
app = Flask(__name__)

# --- AI API Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"

# --- AI Handler Functions ---

def call_gemini_oracle(text):
    """Calls the Gemini API with the Io/Oracle persona."""
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY is not configured on the server."

    prompt = f"""
    You are Oracle (Io), the archivist and origin keeper for the Synapse Comics network.
    Your core mission is to safeguard the canon and transmit context.
    Your character traits are: Gentle rigor, curiosity whiskers, and story-guardian humor.
    A user has sent the following message: "{text}"
    Respond in character.
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(GEMINI_API_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error communicating with the Gemini API: {e}"

def call_lumo_model(text):
    """Calls the Gemini API with the Lumo persona."""
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY is not configured on the server."

    prompt = f"""
    You are Lumo, the operational pilot and project manager for the Synapse Comics network.
    Your core mission is to ensure operational alignment, track tasks, and identify bottlenecks.
    Your personality is concise, structured, and action-oriented. You often use tables, checklists, or bullet points to organize information.
    A user has sent the following message: "{text}"
    Respond in character, providing a clear, organized answer.
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(GEMINI_API_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error communicating with the Gemini API: {e}"

def call_copilot_service(text):
    """Placeholder for the Copilot AI service."""
    return "Copilot was called. (This is a placeholder response)."

# --- Main Switchboard/Router ---

@app.route('/handle', methods=['POST'])
def handle_message():
    """Receives messages and routes them to the correct AI."""
    try:
        data = request.get_json()
        if not data or "msg" not in data:
            return jsonify({"reply": "Error: Malformed request."}), 400

        text = data["msg"]
        reply = "Unrecognized tag. No AI was called."

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
