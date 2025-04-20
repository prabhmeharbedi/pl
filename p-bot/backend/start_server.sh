#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${GREEN}🚀 Starting P-Bot Backend Setup...${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment. Please make sure python3 is installed.${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to activate virtual environment.${NC}"
    exit 1
fi

# Handle the Agno framework
echo -e "${YELLOW}Setting up Agno framework...${NC}"

# The actual agno package is in libs/agno - updated to correct path
AGNO_PACKAGE_DIR="../../framework/agno/libs/agno"
AGNO_PACKAGE_PATH="$(cd "$(dirname "$SCRIPT_DIR")/$AGNO_PACKAGE_DIR" 2>/dev/null && pwd)"

if [ -z "$AGNO_PACKAGE_PATH" ] || [ ! -d "$AGNO_PACKAGE_PATH" ]; then
    echo -e "${RED}Agno framework package not found at $AGNO_PACKAGE_DIR${NC}"
    echo -e "${YELLOW}Trying alternate path...${NC}"
    # Try an alternate path if the first one fails
    AGNO_PACKAGE_DIR="../../framework/agno/libs/agno"
    AGNO_PACKAGE_PATH="$(cd "$SCRIPT_DIR/../../framework/agno/libs/agno" 2>/dev/null && pwd)"
    
    if [ -z "$AGNO_PACKAGE_PATH" ] || [ ! -d "$AGNO_PACKAGE_PATH" ]; then
        echo -e "${RED}Agno framework package not found at alternate path either. Cannot continue.${NC}"
        exit 1
    fi
fi

# Install the Agno framework
echo -e "${YELLOW}Installing Agno framework from local directory...${NC}"
(cd "$AGNO_PACKAGE_PATH" && pip install -e .)
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install Agno framework.${NC}"
    echo -e "${YELLOW}Trying to install with pip directly...${NC}"
    pip install -e "$AGNO_PACKAGE_PATH"
    if [ $? -ne 0 ]; then
        echo -e "${RED}All installation methods failed.${NC}"
        echo -e "${YELLOW}Adding framework to PYTHONPATH as fallback...${NC}"
        export PYTHONPATH="$AGNO_PACKAGE_PATH:$PYTHONPATH"
    fi
fi

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install dependencies.${NC}"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file template...${NC}"
    echo "OPENAI_API_KEY=your_openai_api_key" > .env
    echo "ANTHROPIC_API_KEY=your_anthropic_api_key" >> .env
    echo -e "${RED}⚠️ Please edit the .env file to add your API keys before starting the server.${NC}"
    exit 1
fi

# Create necessary directories
echo -e "${YELLOW}Setting up directories...${NC}"
mkdir -p uploads tmp/lancedb knowledge/tenancy

# Start server
echo -e "${GREEN}Starting P-Bot backend server...${NC}"
echo -e "${YELLOW}The server will be available at http://localhost:8000${NC}"
PYTHONPATH="$AGNO_PACKAGE_PATH:$PYTHONPATH" uvicorn main:app --host 0.0.0.0 --port 8000 --reload 