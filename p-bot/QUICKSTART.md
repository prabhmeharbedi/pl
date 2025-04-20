# P-Bot Quick Start Guide

This guide will help you quickly start the P-Bot real estate assistant application on macOS.

## Prerequisites

- macOS operating system
- Python 3.8+ installed
- Node.js and npm installed (for frontend)
- Access to OpenAI and Anthropic API keys

## Getting Started

There are three ways to start P-Bot, depending on your needs:

### Option 1: All-in-One Starter (Recommended)

1. Double-click the `Start_P-Bot.command` file in the p-bot directory
2. This will open two terminal windows, one for the backend and one for the frontend
3. The first time you run this, it will set up virtual environments and install dependencies
4. If you don't have API keys configured, it will prompt you to add them

### Option 2: Backend Only

1. Double-click the `Start_P-Bot_Server.command` file in the p-bot directory
2. This will start only the backend server
3. The API will be available at http://localhost:8000

### Option 3: Frontend Only

1. Double-click the `Start_P-Bot_Frontend.command` file in the p-bot directory
2. This will start only the frontend application
3. The web interface will be available at http://localhost:5173
4. Note: The frontend requires the backend to be running to function properly

## API Keys Setup

On first run, the backend starter will create a `.env` file in the `backend` directory. You need to edit this file to add your API keys:

```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

The `.env` file is located at: `/Users/ssbedi/Desktop/pl/p-bot/backend/.env`

## Accessing the Application

- Web Interface: http://localhost:5173
- API Documentation: http://localhost:8000/docs

## Troubleshooting

If you encounter issues with the framework installation, you can try the manual setup helper:

1. Open Terminal
2. Navigate to the backend directory:
   ```bash
   cd /Users/ssbedi/Desktop/pl/p-bot/backend
   ```
3. Run the manual setup helper:
   ```bash
   ./manually_setup_env.sh
   ```
4. Follow the prompts - this will:
   - Detect available framework paths
   - Install dependencies
   - Create a custom runner script
   - Give you the option to start the server

Other common issues:

1. Check the terminal windows for error messages
2. Ensure you have the correct Python and Node.js versions installed
3. Make sure your API keys are correctly set in the `.env` file
4. Verify that both the backend and frontend are running

## Framework Structure

The Agno framework path appears to be at:
```
/Users/ssbedi/Desktop/pl/framework/agno/libs/agno
```

If you encounter "module not found" errors, you'll need to ensure this directory is in your Python path.

## Manual Setup (Alternative)

If the starter scripts don't work for you, you can manually set up the application:

### Backend Manual Setup
```bash
cd p-bot/backend
python -m venv venv
source venv/bin/activate
# Add framework to Python path
export PYTHONPATH="/Users/ssbedi/Desktop/pl/framework/agno/libs/agno:$PYTHONPATH"
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Manual Setup
```bash
cd p-bot/frontend
npm install
npm run dev
``` 