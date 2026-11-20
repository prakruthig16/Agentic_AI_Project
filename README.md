# Agentic AI Assistant

An AI-powered conversational assistant built using Python, Django, and Ollama.

## Overview

A web-based AI assistant with a Django backend and locally hosted language model integration.

## Features

- AI-powered conversational interface
- Django-based backend
- Local LLM integration using Ollama
- Interactive chat interface
- Dashboard
- Conversation history
- Structured data handling

## Tech Stack

- Python
- Django
- Ollama
- HTML, CSS, JavaScript
- SQLite

## Project Structure

- config/manage.py
- config/assistant/ai_engine.py
- config/assistant/views.py
- config/assistant/models.py
- config/assistant/schemas.py
- config/templates/
- config/static/

## Installation

1. Clone the repository:

   `git clone https://github.com/prakruthig16/Agentic_AI_Project.git`

2. Navigate to the Django project:

   `cd Agentic_AI_Project/config`

3. Create and activate a virtual environment:

   `python -m venv venv`

   `.\venv\Scripts\Activate`

4. Install dependencies:

   `python -m pip install django ollama`

5. Install Ollama from https://ollama.com/ and download the model configured in `assistant/ai_engine.py`.

6. Run migrations:

   `python manage.py migrate`

7. Start the server:

   `python manage.py runserver`

8. Open http://127.0.0.1:8000/

## Future Improvements

- Persistent conversational memory
- Multi-agent workflows
- Multiple LLM support
- User authentication
- Automated testing
- Cloud deployment

## Author

Prakruthi G

GitHub: https://github.com/prakruthig16

Project: https://github.com/prakruthig16/Agentic_AI_Project
