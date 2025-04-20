#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the backend directory
cd "$SCRIPT_DIR/backend"

# Execute the startup script
./start_server.sh

# Keep terminal open in case of error
read -p "Press enter to close this window..." 