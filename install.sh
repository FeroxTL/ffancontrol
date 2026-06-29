#!/bin/bash

set -e

echo "Installing ffancontrol..."

# Copy the script
sudo cp ffancontrol.py /usr/local/bin/ffancontrol.py
sudo chmod +x /usr/local/bin/ffancontrol.py

# Install the systemd service
sudo cp systemd/ffancontrol.service /etc/systemd/system/ffancontrol.service
sudo cp systemd/ffancontrol.timer /etc/systemd/system/ffancontrol.timer

# Reload systemd and enable the service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable ffancontrol.service
sudo systemctl enable ffancontrol.timer

# Optional: start ffancontrol if not done
sudo systemctl start ffancontrol.service
sudo systemctl start ffancontrol.timer

echo "Installation complete."
