import os
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # Import CORS
from pyngrok import ngrok, conf  # Import ngrok and conf

class Agent:
    def __init__(self, host="0.0.0.0", port=5001, cors_allowed_origins="*", ssl_context=None):
        """Initialize the Flask app and SocketIO"""
        self.app = Flask(__name__)
        
        # Enable CORS for the Flask app
        CORS(self.app, resources={r"/*": {"origins": cors_allowed_origins}})
        
        # Initialize SocketIO with CORS allowed origins for WebSocket connections
        self.socketio = SocketIO(self.app, cors_allowed_origins=cors_allowed_origins)
        self.host = host
        self.port = port
        self.message_handler = None  # Placeholder for user-defined message handler
        self.ngrok_tunnel = None  # Placeholder for the Ngrok tunnel
        self.ssl_context = ssl_context

        # Register event handler for user messages
        self.socketio.on_event('user_message', self._handle_user_message)

    def on_message(self, handler):
        """Set the function that handles user messages"""
        self.message_handler = handler

    def _handle_user_message(self, message):
        """Internal method to handle incoming messages"""
        print(f"Received message: {message}")
        
        # Check if a user-defined message handler is set
        if self.message_handler:
            self.message_handler(message)  # Delegate the message handling to the user-defined function
        else:
            print("No message handler defined!")

    def send_message(self, message):
        """Send a message to the client"""
        emit('bot_response', message)

    def start_typing(self):
        """Emit typing start event to the client"""
        emit('agent_typing')

    def stop_typing(self):
        """Emit typing stop event to the client"""
        emit('agent_stop_typing')

    def run(self, debug=True, ngrok_token=None):
        """Start the SocketIO server, disable reloader if Ngrok is enabled"""
        
        # Disable the reloader if ngrok_token is provided, to prevent changing URLs
        if ngrok_token:
            debug = False  # Disable reloader as we don't want ngrok URL to change with every restart
            conf.get_default().auth_token = ngrok_token  # Set the auth token
            self.ngrok_tunnel = ngrok.connect(self.port)
            print(f"Ngrok tunnel available at: {self.ngrok_tunnel.public_url}")

        print(f"Server running locally at http://{self.host}:{self.port}")

        # Flask-SocketIO automatically manages threading and reloading when debug=True
        self.socketio.run(self.app, host=self.host, port=self.port, use_reloader=debug, allow_unsafe_werkzeug=True, ssl_context=self.ssl_context)

    def stop_ngrok(self):
        """Stop the Ngrok tunnel"""
        if self.ngrok_tunnel:
            ngrok.disconnect(self.ngrok_tunnel.public_url)
            print(f"Ngrok tunnel {self.ngrok_tunnel.public_url} stopped")
