#!/bin/bash
# Set variables with defaults from environment if available
FACTORY="${FACTORY:-demo-ai}"   # Use environment variable if set, otherwise default
TOKEN="${TOKEN}"                # Required, should be set by environment
# Check if TOKEN is set
if [ -z "$TOKEN" ]; then
    echo "ERROR: TOKEN environment variable is not set"
    exit 4
fi


# Function to exit with status and message
exit_with_status() {
    local status=$1
    local message=$2
    echo "$message"
    exit $status
}

print_update() {
    echo "=============================="
    echo "Atualizando de: $1"
    echo "              para: $2"
    echo "=============================="
}

# ------------------------------
# LOAD CONFIGURATION FROM FILE
# ------------------------------
CONFIG_FILE="/run/secrets/light-config"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"  # Load variables from config file
fi

# Set default UPDATE_TIME if not defined in config
UPDATE_TIME="${UPDATE_TIME:-5}"  # Defaults to 5 if unset
DEVICE="${DEVICE:-device1}"  # Use environment variable if set, otherwise default

# Apps (these can be overridden by the config file)
APP1="${APP1:-edge-impulse-object-detection}"
APP2="${APP2:-gst-ai-face-detection}"
APP3="${APP3:-gst-concurrent-videoplay-composition}"

# Debug: Print environment variables (remove in production)
echo "DEVICE: $DEVICE"
echo "FACTORY: $FACTORY"
echo "TOKEN: ${TOKEN:0:10}..."  # Only show first 10 chars of token for security

echo "APP1: $APP1"
echo "APP2: $APP2"
echo "APP3: $APP3"

FIOCTL_CMD_DEV="$DEVICE -f $FACTORY -t $TOKEN"

# Get the latest configuration timestamp
latest_timestamp=$(fioctl devices config log $FIOCTL_CMD_DEV | grep "Created At:" | head -1 | awk '{print $3}')
# Check if we got a timestamp
if [ -z "$latest_timestamp" ]; then
    exit_with_status 4 "ERROR: Failed to get configuration timestamp"
fi
# Convert to Unix timestamp
config_timestamp=$(date -d "$latest_timestamp" +%s)
# Get current device time
current_timestamp=$(date +%s)

# Calculate difference in seconds
diff_seconds=$((current_timestamp - config_timestamp))

# Check if difference is more than UPDATE_TIME 
if [ "$diff_seconds" -le "$UPDATE_TIM" ]; then
    exit_with_status 1 "Update not available yet (Time: $diff_seconds seconds)"
fi

# Get device apps
apps_output=$(fioctl devices list --columns apps $FIOCTL_CMD_DEV)
echo "=============================="
echo "apps_output: $apps_output"
echo "=============================="

# Check if we got apps output
if [ -z "$apps_output" ]; then
    exit_with_status 4 "ERROR: Failed to get device apps"
fi
# Extract the apps line (skip header and separator)
apps_line=$(echo "$apps_output" | tail -n +3 | head -n 1)

# Check for specific apps and update accordingly
if [[ "$apps_line" == *"$APP1"* ]]; then
    print_update "$APP1" "$APP2"
    new_apps=$(echo "$apps_line" | sed "s/$APP1/$APP2/g")
    update_output=$(fioctl devices config updates $FIOCTL_CMD_DEV --apps "$new_apps" 2>&1)
    if [ $? -eq 0 ]; then
        exit_with_status 0 "DEV: Successfully updated"
    else
        exit_with_status 5 "ERROR updating"
    fi

elif [[ "$apps_line" == *"$APP2"* ]]; then
    print_update "$APP2" "$APP3"
    new_apps=$(echo "$apps_line" | sed "s/$APP2/$APP3/g")
    update_output=$(fioctl devices config updates $FIOCTL_CMD_DEV --apps "$new_apps" 2>&1)
    if [ $? -eq 0 ]; then
        exit_with_status 0 "DEV: Successfully updated"
    else
        exit_with_status 5 "ERROR updating"
    fi

elif [[ "$apps_line" == *"$APP3"* ]]; then
    print_update "$APP3" "$APP1"
    new_apps=$(echo "$apps_line" | sed "s/$APP3/$APP1/g")
    update_output=$(fioctl devices config updates $FIOCTL_CMD_DEV --apps "$new_apps" 2>&1)
    if [ $? -eq 0 ]; then
        exit_with_status 0 "DEV: Successfully updated"
    else
        exit_with_status 5 "ERROR updating"
    fi
else
    exit_with_status 2 "Device is running other apps: $apps_line"
fi