# P-Bot Real Estate Assistant

P-Bot is a multi-agent real estate chatbot system built using the Agno framework. It provides a full-stack application with specialized AI agents for property issues and tenancy questions.

## Features

### Issue Detection & Troubleshooting Agent
- Analyzes uploaded property images to identify issues (mold, water damage, cracks, etc.)
- Provides troubleshooting advice and recommendations
- Suggests appropriate professionals to contact for serious issues
- Asks clarifying questions to better diagnose problems

### Tenancy FAQ Agent
- Answers questions about tenancy laws, rental agreements, and tenant/landlord responsibilities
- Provides location-specific guidance when a location is provided
- Offers advice on common issues like security deposits, eviction processes, and rent increases
- Uses a knowledge base of tenancy information for accurate responses

### Multi-Agent Architecture
- Automatic router agent that directs queries to the appropriate specialized agent
- Natural conversation flow with the ability to switch between agents
- Persistent session memory for continuous conversations

## Project Structure

- `backend/`: FastAPI server and Agno agent implementation
- `frontend/`: React web application

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Create a `.env` file in the backend directory
- Add your API keys:
```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

5. Run the server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Usage

1. Access the web interface at `http://localhost:5173`
2. Choose a specialized agent or start typing a question
3. For property issues, upload an image using the image upload button
4. For tenancy questions, provide your location for more accurate information
5. Continue the conversation with follow-up questions

## Development

- Backend API available at `http://localhost:8000`
- Frontend development server runs at `http://localhost:5173`
- API documentation available at `http://localhost:8000/docs`

## Technologies Used

- **Backend**:
  - FastAPI
  - Agno Framework
  - OpenAI Models (with vision capabilities)
  - LanceDB for knowledge base

- **Frontend**:
  - React
  - Tailwind CSS
  - React Dropzone for image uploads 