_#!/bin/bash

# Setup Script for Task 3: Azurite Installation and Configuration
# This script automates the setup of Azurite for local Azure Blob Storage simulation

echo "=========================================="
echo "Task 3: Azurite Setup Script"
echo "=========================================="
echo ""

# Check if running in WSL
if grep -qi microsoft /proc/version; then
    echo "✓ Running in WSL environment"
else
    echo "⚠ Warning: Not running in WSL. Proceeding anyway..."
fi

echo ""
echo "Step 1: Installing required Python packages..."
echo "--------------------------------------------"

# Install required Python packages
pip3 install --break-system-packages azure-storage-blob pandas

echo ""
echo "Step 2: Installing Azurite..."
echo "--------------------------------------------"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm not found. Installing Node.js and npm..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Install Azurite globally
echo "Installing Azurite via npm..."
sudo npm install -g azurite

echo ""
echo "Step 3: Creating project directory structure..."
echo "--------------------------------------------"

# Create necessary directories
mkdir -p azurite_data
mkdir -p simulated_nosql

echo "✓ Created azurite_data/ for Azurite storage"
echo "✓ Created simulated_nosql/ for results storage"

echo ""
echo "Step 4: Creating helper scripts..."
echo "--------------------------------------------"

# Create script to start Azurite
cat > start_azurite.sh << 'EOF'
#!/bin/bash
echo "Starting Azurite Blob Storage Emulator..."
azurite --silent --location azurite_data --debug azurite_data/debug.log &
AZURITE_PID=$!
echo "Azurite started with PID: $AZURITE_PID"
echo $AZURITE_PID > azurite_data/azurite.pid
echo "Azurite is running on:"
echo "  Blob Service: http://127.0.0.1:10000"
echo ""
echo "To stop Azurite, run: ./stop_azurite.sh"
EOF

chmod +x start_azurite.sh

# Create script to stop Azurite
cat > stop_azurite.sh << 'EOF'
#!/bin/bash
if [ -f azurite_data/azurite.pid ]; then
    PID=$(cat azurite_data/azurite.pid)
    echo "Stopping Azurite (PID: $PID)..."
    kill $PID 2>/dev/null
    rm azurite_data/azurite.pid
    echo "Azurite stopped."
else
    echo "No Azurite PID file found. Attempting to kill any running Azurite processes..."
    pkill -f azurite
    echo "Done."
fi
EOF

chmod +x stop_azurite.sh

# Create Python script to upload CSV to Azurite
cat > upload_to_azurite.py << 'EOF'
"""
Helper script to upload All_Diets.csv to Azurite Blob Storage
"""
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import sys

def upload_csv_to_azurite(csv_path):
    # Azurite connection string
    connect_str = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )
    
    try:
        # Create BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        
        # Create container
        container_name = 'datasets'
        try:
            container_client = blob_service_client.create_container(container_name)
            print(f"✓ Created container: {container_name}")
        except ResourceExistsError:
            print(f"✓ Container already exists: {container_name}")
            container_client = blob_service_client.get_container_client(container_name)
        
        # Upload blob
        blob_name = 'All_Diets.csv'
        blob_client = container_client.get_blob_client(blob_name)
        
        print(f"Uploading {csv_path} to Azurite...")
        with open(csv_path, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)
        
        print(f"✓ Successfully uploaded {blob_name} to container {container_name}")
        print(f"  Blob URL: http://127.0.0.1:10000/devstoreaccount1/{container_name}/{blob_name}")
        
    except FileNotFoundError:
        print(f"✗ Error: File not found: {csv_path}")
        print("  Please make sure All_Diets.csv is in the current directory")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = "All_Diets.csv"
    
    upload_csv_to_azurite(csv_path)
EOF

echo "✓ Created start_azurite.sh"
echo "✓ Created stop_azurite.sh"
echo "✓ Created upload_to_azurite.py"

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Make sure All_Diets.csv is in this directory"
echo "2. Start Azurite: ./start_azurite.sh"
echo "3. Upload CSV: python3 upload_to_azurite.py"
echo "4. Run serverless function: python3 lambda_function.py"
echo "5. Stop Azurite: ./stop_azurite.sh"
echo ""