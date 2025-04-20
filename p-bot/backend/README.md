# P-Bot Backend

This is the backend component of the P-Bot multi-agent real estate chatbot system built using the Agno framework.

## Recent Fixes

1. Fixed syntax error in `requirements.txt` (pandas=2.2.3 → pandas==2.2.3)
2. Updated memory implementation to use ThreadMemory instead of AgentMemory
3. Added proper directory creation for knowledge and uploads
4. Improved error handling in knowledge loading process
5. Fixed image processing format for OpenAI vision models
6. Implemented better exception handling

## Getting Started

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the local Agno framework:
```bash
cd ../../framework/agno
pip install -e .
cd ../../p-bot/backend
```

3. Install other dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the backend directory with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

5. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000 with documentation at http://localhost:8000/docs

## Project Structure

- `main.py`: FastAPI server entry point
- `agent.py`: P-Bot agent implementation
- `api/`: API routes
- `config/`: Configuration settings
- `utils/`: Utility functions
- `knowledge/`: Knowledge base for the chatbot 