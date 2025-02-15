# Intent-based Information Retrieval Software for Data Lifecycle Management

This software is part of the modules of a project on Intent-based Data Lifecyle Management. 
The functionalities of the software include providing users with a chat interface through which they can query custom datasets in defined domains and not in the internet.
It also has an intent-based model selection component that recommends suitable LLMs for processing user queries based on user-defined preferences from models, computing resources analysis, and evaluation of other model properties.
The metrics applied by the component to select these models are: latency, memory usage, accuracy, recall, precision, cross-lingual ability, and verbosity. 
The focus of the research is the analysis and recommendation of the models with these metrics.

## Installation

- Download the application code:
    ```
    git clone https://github.com/tissadeking/chat.git
    ```
- Enter the project directory.
    ```
    cd chat

- Install the requirements and run the app:
    ```
    pip install -r requirements.txt
    python3 chat_flask.py
    ```
## Accessing the chat interface
- The software becomes available at http://127.0.0.1:5002.

