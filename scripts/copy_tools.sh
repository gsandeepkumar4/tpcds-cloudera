#!/bin/bash

# Ensure the script exits if any command fails
set -e

# Check if both username and hosts are provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <USERNAME> <HOSTS>"
    echo "Example: $0 gsandeepkumar 98.80.153.69,98.80.153.70"
    exit 1
fi

# Variables
USERNAME=$1    # Regular user for SSH (passed as argument)
HOSTS=$2       # Comma-separated list of remote hosts

LOCAL_TOOLS_ZIP="tpcds_tools.zip"  # Update with actual path of tools.zip on local machine
SHARED_DIR="/data/"                # Shared directory where tools will be extracted
TOOLS_ZIP="/tmp/tools.zip"         # Temporary location for tools.zip on the remote host

IFS=','
read -ra all_hosts <<< "$HOSTS"

# Iterate over each host
for host in "${all_hosts[@]}"
do
  echo "Processing host: $host"

  # Step 1: SSH into the host and prepare the destination directory (prompts for password)
  ssh $USERNAME@$host << EOF
    sudo bash -c '
      # Remove the existing tools directory if it exists
      rm -rf $SHARED_DIR

      # Create a new shared tools directory
      mkdir -p $SHARED_DIR
    '
EOF

  # Step 2: Copy tools.zip from the local system to the remote host (prompts for password)
  echo "Copying tools.zip to $host..."
  scp "$LOCAL_TOOLS_ZIP" $USERNAME@$host:$TOOLS_ZIP

  # Step 3: SSH again to extract tools.zip and set permissions (prompts for password)
  ssh $USERNAME@$host << EOF
    sudo bash -c '
      # Extract tools.zip into the shared directory
      unzip -q $TOOLS_ZIP -d $SHARED_DIR

      # Set permissions to allow all users full access
      chmod -R 777 $SHARED_DIR

      # Remove the zip file after extraction
      rm -f $TOOLS_ZIP

      echo "Tools successfully extracted to $host at $SHARED_DIR"
    '
EOF

done

echo "Script execution completed!"
