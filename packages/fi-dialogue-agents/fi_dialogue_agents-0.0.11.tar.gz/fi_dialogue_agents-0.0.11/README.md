# Build FI Dialogue Agents

`fi_dialogue_agents` is a Python package that simplifies creating dialogue agents using Flask and Socket.IO for **FI Dialogue**. This wrapper makes it easy to build and deploy agents with minimal configuration, and even allows public access via ngrok reverse tunneling.

## Installation

To install the package, simply run:

```bash
pip install fi_dialogue_agents
```

## Usagea

Once installed, you can use the `Agent` class to build your own dialogue agents. Below is a quick guide on initializing agents, handling messages, and running the server.

### 1. Agent Initialization

The `Agent` class is the core of this package. Initialize an agent by specifying the `host` and `port` for the Flask server:

```python
from fi_dialogue_agents import Agent

# Create an instance of the Agent
agent = Agent(host="0.0.0.0", port=5001)
```

### 2. Handling Incoming Messages

You can define a custom message handler using the `on_message` method. This function is triggered whenever a message is received from the client.

```python
def handle_user_message(message):
    print(f"Handling message: {message}")
    agent.send_message(f"Echo: {message}")

# Set the custom message handler
agent.on_message(handle_user_message)
```

### 3. Running the Server

You can either run the server locally or expose it publicly via ngrok.

#### a. Running Locally

To start the server locally, use the following command:

```python
agent.run()
```

#### b. Running with Ngrok

If you want to expose the server publicly, you can use ngrok. Pass your ngrok authentication token to the `run` method:

```python
agent.run(debug=True, ngrok_token="<your_ngrok_token>")
```

You can obtain your ngrok token from [ngrok's website](https://ngrok.com/).

### 4. Running the Agent Script

To start the agent, run the following command in your terminal:

```bash
python agent.py
```

This will start the server and, if ngrok is used, provide both the local and public URLs. Hot-reloading is enabled by default, but it is disabled when ngrok is used to prevent generating multiple public URLs.

If you'd like to run the agent as a background process, you can use the `nohup` command:

```bash
nohup python agent.py > output.log 2>&1 &
```

The server logs, including the ngrok URL, will be saved to `output.log`.

## API Reference

### Agent Class

`Agent(host, port, cors_allowed_origins)`: Initializes a new Flask-SocketIO agent.

- `host`: The hostname for the Flask server (default: "0.0.0.0").
- `port`: The port to run the server (default: 5001).

- `on_message(handler)`: Set a custom handler for user messages.

  - `handler`: A function that will be called with the incoming message as its argument.

- `send_message(message)`: Sends a message to the client.

  - `message`: The message to send back to the client.

- `start_typing()`: Sends a typing notification to the client.

- `stop_typing()`: Stops the typing notification.

- `run(debug=True, ngrok_token=None)`: Starts the Flask-SocketIO server.
  - `debug`: Whether to run the server in debug mode.
  - `ngrok_token`: If provided, the server will be exposed to the public via an Ngrok tunnel.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
