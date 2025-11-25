#!/bin/bash

PROJECT_DIR="/Users/macpc/Developer/cpi_estimate"
SCRIPT_PATH="$PROJECT_DIR/run_scheduler.sh"

echo "To schedule the CPI forecast update to run daily at 9:00 AM (checking if it's the 30th internally):"
echo ""
echo "1. Open your crontab for editing:"
echo "   crontab -e"
echo ""
echo "2. Add the following line to the end of the file:"
echo "   0 9 * * * $SCRIPT_PATH"
echo ""
echo "3. Save and exit."
