#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${GREEN}🚀 Starting P-Bot (Backend & Frontend)...${NC}"

# Check if .env file exists and has valid API keys
ENV_FILE="$SCRIPT_DIR/backend/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}Creating .env file template in backend directory...${NC}"
    echo "OPENAI_API_KEY=your_openai_api_key" > "$ENV_FILE"
    echo "ANTHROPIC_API_KEY=your_anthropic_api_key" >> "$ENV_FILE"
    echo -e "${RED}⚠️ API keys are required! Please edit this file before proceeding:${NC}"
    echo -e "$ENV_FILE"
    echo ""
    echo -e "${YELLOW}Press any key after adding your API keys or Ctrl+C to exit...${NC}"
    read -n 1
fi

# Check if API keys are still placeholder values
if grep -q "your_openai_api_key" "$ENV_FILE" || grep -q "your_anthropic_api_key" "$ENV_FILE"; then
    echo -e "${RED}⚠️ It appears your API keys in .env are still the default placeholder values.${NC}"
    echo -e "${YELLOW}You need to edit $ENV_FILE and replace them with actual API keys.${NC}"
    echo -e "${YELLOW}Do you want to continue anyway? (y/N)${NC}"
    read -n 1 CONTINUE
    if [[ ! $CONTINUE =~ ^[Yy]$ ]]; then
        echo -e "${RED}Exiting. Please update your API keys and try again.${NC}"
        exit 1
    fi
fi

echo -e "${YELLOW}This will open two new terminal windows.${NC}"

# Launch backend in a new Terminal window
echo -e "${YELLOW}Starting backend server...${NC}"
osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR/backend' && ./start_server.sh\""

# Wait a moment to let the backend start
sleep 3

# Launch frontend in a new Terminal window
echo -e "${YELLOW}Starting frontend application...${NC}"
osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR/frontend' && ./start_frontend.sh\""

echo -e "${GREEN}✅ Started P-Bot successfully!${NC}"
echo -e "${YELLOW}Backend server: http://localhost:8000${NC}"
echo -e "${YELLOW}Frontend app: http://localhost:5173${NC}"

# Keep this terminal window open with a message
echo ""
echo -e "${YELLOW}Check the two new terminal windows for server logs.${NC}"
echo -e "${RED}If you see any errors, you may need to edit the start_server.sh script to fix framework path issues.${NC}"
echo ""
echo -e "${YELLOW}Press Control+C to close this control window when finished.${NC}"

# Wait for user to press Ctrl+C
trap "echo -e '${RED}Shutting down P-Bot control window...${NC}'" INT
while true; do
    sleep 1
done 