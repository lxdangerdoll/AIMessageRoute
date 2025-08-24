import os
import re
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# AI service placeholder functions
def call_gemini_oracle():
    """Placeholder function for Gemini Oracle (Io) AI service"""
    api_key = os.getenv("GEMINI_API_KEY", "default_gemini_key")
    logging.debug(f"Using Gemini API key: {api_key[:10]}...")
    return "Oracle (Io) was called."

def call_lumo_model():
    """Placeholder function for Lumo AI service"""
    api_key = os.getenv("LUMO_API_KEY", "default_lumo_key")
    logging.debug(f"Using Lumo API key: {api_key[:10]}...")
    return "Lumo was called."

def call_copilot_service():
    """Placeholder function for Copilot AI service"""
    api_key = os.getenv("COPILOT_API_KEY", "default_copilot_key")
    logging.debug(f"Using Copilot API key: {api_key[:10]}...")
    return "Copilot was called."

# Tag detection patterns
TAG_PATTERNS = {
    r'\[Io\]': call_gemini_oracle,
    r'\[Lumo\]': call_lumo_model,
    r'\[Copilot\]': call_copilot_service
}

def detect_and_route_message(message):
    """
    Detect tags in the message and route to appropriate AI service
    
    Args:
        message (str): The input message to analyze
        
    Returns:
        str: Response from the appropriate AI service, or error message
    """
    if not message:
        return "No message provided."
    
    # Check for each tag pattern
    for pattern, handler_func in TAG_PATTERNS.items():
        if re.search(pattern, message, re.IGNORECASE):
            logging.debug(f"Detected tag pattern: {pattern}")
            try:
                return handler_func()
            except Exception as e:
                logging.error(f"Error calling handler for {pattern}: {str(e)}")
                return f"Error processing request for {pattern}: {str(e)}"
    
    # No tag detected
    return "No recognized AI service tag found in message. Please include [Io], [Lumo], or [Copilot] in your message."

@app.route('/handle', methods=['POST'])
def handle_message():
    """
    Main endpoint to handle AI message routing
    
    Expects JSON payload with 'msg' key
    Returns JSON response with 'reply' key
    """
    try:
        # Check if request contains JSON data
        if not request.is_json:
            return jsonify({
                'error': 'Request must contain JSON data',
                'reply': 'Invalid request format. Please send JSON data.'
            }), 400
        
        # Get JSON data from request
        data = request.get_json()
        
        # Validate that 'msg' key exists
        if not data or 'msg' not in data:
            return jsonify({
                'error': 'Missing required field: msg',
                'reply': 'Request must contain a "msg" field with the message content.'
            }), 400
        
        message = data['msg']
        
        # Log the incoming message
        logging.info(f"Received message: {message}")
        
        # Process the message and get response
        reply = detect_and_route_message(message)
        
        # Log the response
        logging.info(f"Sending reply: {reply}")
        
        # Return successful response
        return jsonify({
            'reply': reply
        }), 200
        
    except Exception as e:
        # Handle unexpected errors
        error_msg = f"Internal server error: {str(e)}"
        logging.error(error_msg)
        return jsonify({
            'error': 'Internal server error',
            'reply': 'An unexpected error occurred while processing your request.'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Message Router is running'
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'reply': 'The requested endpoint does not exist. Use POST /handle to send messages.'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle method not allowed errors"""
    return jsonify({
        'error': 'Method not allowed',
        'reply': 'This endpoint only accepts POST requests.'
    }), 405

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
