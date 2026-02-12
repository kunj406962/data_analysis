from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import sys

def upload_csv_to_azurite():
    csv_path = "res/csv/All_Diets.csv"
    
    connect_str = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = 'datasets'
        try:
            container_client = blob_service_client.create_container(container_name)
            print(f"✓ Created container: {container_name}")
        except ResourceExistsError:
            print(f"✓ Container already exists: {container_name}")
            container_client = blob_service_client.get_container_client(container_name)
        
        blob_name = 'All_Diets.csv'
        blob_client = container_client.get_blob_client(blob_name)
        
        print(f"Uploading {csv_path} to Azurite...")
        with open(csv_path, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)
        
        print(f"✓ Successfully uploaded {blob_name} to container {container_name}")
        print(f"  Blob URL: http://127.0.0.1:10000/devstoreaccount1/{container_name}/{blob_name}")
        
    except FileNotFoundError:
        print(f"✗ Error: File not found: {csv_path}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    
    upload_csv_to_azurite()
