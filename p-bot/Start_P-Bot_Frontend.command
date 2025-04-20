#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the frontend directory
cd "$SCRIPT_DIR/frontend"

# Execute the startup script
./start_frontend.sh

# Keep terminal open in case of error
read -p "Press enter to close this window..." 