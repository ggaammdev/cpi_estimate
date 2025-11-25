#!/bin/bash

# Navigate to the project directory
PROJECT_DIR="/Users/macpc/Developer/cpi_estimate"
cd "$PROJECT_DIR" || exit 1

# Log file path
LOG_FILE="$PROJECT_DIR/scheduler.log"

# Log start time
echo "----------------------------------------------------------------" >> "$LOG_FILE"
echo "Running scheduler at $(date)" >> "$LOG_FILE"

# Run the scheduler script
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 scheduler.py >> "$LOG_FILE" 2>&1

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Scheduler finished successfully at $(date)" >> "$LOG_FILE"
else
    echo "Scheduler failed with exit code $EXIT_CODE at $(date)" >> "$LOG_FILE"
fi
