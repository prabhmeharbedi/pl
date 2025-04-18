# P-Bot Backend

This is the backend for P-Bot, an AI-powered chatbot built using the Agno framework.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Create a `.env` file in the backend directory
- Add your API keys:
```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

4. Run the server:
```bash
uvicorn main:app --reload
```

## Project Structure

- `main.py`: FastAPI server entry point
- `agent.py`: P-Bot agent implementation
- `api/`: API routes
- `config/`: Configuration settings
- `utils/`: Utility functions
- `knowledge/`: Knowledge base for the chatbot 