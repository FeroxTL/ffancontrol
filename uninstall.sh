#!/bin/bash

set -e

SERVICE_NAME="ffancontrol"
SCRIPT_PATH="/usr/local/bin/ffancontrol.py"
UNIT_PATH="/etc/systemd/system/$SERVICE_NAME"

echo "Stopping $SERVICE_NAME.service..."
sudo systemctl stop "$SERVICE_NAME.service" || echo "Service not running."

echo "Stopping $SERVICE_NAME.timer..."
sudo systemctl stop "$SERVICE_NAME.timer" || echo "Timer not running."

echo "Disabling $SERVICE_NAME.service..."
sudo systemctl disable "$SERVICE_NAME.service" || echo "Service not enabled."

echo "Disabling $SERVICE_NAME.timer..."
sudo systemctl disable "$SERVICE_NAME.timer" || echo "Timer not enabled."

echo "Removing script: $SCRIPT_PATH"
sudo rm -f "$SCRIPT_PATH"

echo "Removing systemd service unit: $UNIT_PATH.service"
sudo rm -f "$UNIT_PATH.service"

echo "Removing systemd timer unit: $UNIT_PATH.timer"
sudo rm -f "$UNIT_PATH.timer"

echo "Reloading systemd..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload

echo "✅ Uninstallation complete."
