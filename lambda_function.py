from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json
import os
from datetime import datetime

def process_nutritional_data_from_azurite():
    print(f"[{datetime.now()}] Starting nutritional data processing...")
    
    connect_str = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        print(f"[{datetime.now()}] Connected to Azurite Blob Storage")
        
        container_name = 'datasets'
        blob_name = 'All_Diets.csv'
        
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        
        print(f"[{datetime.now()}] Downloading blob: {blob_name}")
        stream = blob_client.download_blob().readall()
        df = pd.read_csv(io.BytesIO(stream))
        
        print(f"[{datetime.now()}] Successfully loaded {len(df)} records from CSV")
        print(f"[{datetime.now()}] Cleaning data...")
        df.fillna(df.mean(numeric_only=True), inplace=True)
        
        print(f"[{datetime.now()}] Calculating average macronutrients by diet type...")
        avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
        
        print(f"[{datetime.now()}] Calculating additional metrics...")
        
        # Top 5 protein-rich recipes per diet type
        top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
        
        # Convert to a serializable format
        top_protein_summary = {}
        for diet_type in df['Diet_type'].unique():
            diet_data = top_protein[top_protein['Diet_type'] == diet_type][['Recipe_name', 'Protein(g)']].head(5)
            top_protein_summary[str(diet_type)] = diet_data.to_dict('records')
        
        # Diet type with highest average protein
        highest_protein_diet = avg_macros['Protein(g)'].idxmax()
        highest_protein_value = avg_macros['Protein(g)'].max()
        
        # Most common cuisines per diet type
        common_cuisines = {}
        for diet_type in df['Diet_type'].unique():
            cuisine_counts = df[df['Diet_type'] == diet_type]['Cuisine_type'].value_counts().head(3)
            common_cuisines[str(diet_type)] = cuisine_counts.to_dict()
        
        # Recipe count per diet type
        recipe_counts = df.groupby('Diet_type').size().to_dict()
        recipe_counts = {str(k): int(v) for k, v in recipe_counts.items()}
        
        # Create comprehensive results dictionary
        results = {
            'processing_timestamp': datetime.now().isoformat(),
            'total_recipes_processed': int(len(df)),
            'diet_types_analyzed': int(len(avg_macros)),
            'average_macronutrients_by_diet': avg_macros.reset_index().to_dict('records'),
            'top_protein_recipes_by_diet': top_protein_summary,
            'highest_protein_diet': {
                'diet_type': str(highest_protein_diet),
                'average_protein_g': float(highest_protein_value)
            },
            'common_cuisines_by_diet': common_cuisines,
            'recipe_counts_by_diet': recipe_counts
        }
        
        os.makedirs('simulated_nosql', exist_ok=True)
        
        output_path = 'simulated_nosql/results.json'
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"[{datetime.now()}] Results saved to {output_path}")
        
        print("\n" + "="*60)
        print("PROCESSING SUMMARY")
        print("="*60)
        print(f"Total recipes processed: {len(df)}")
        print(f"Diet types analyzed: {len(avg_macros)}")
        print(f"Highest protein diet: {highest_protein_diet} ({highest_protein_value:.2f}g)")
        print(f"Results saved to: {output_path}")
        print("="*60 + "\n")
        
        return "Data processed and stored successfully."
        
    except Exception as e:
        error_msg = f"[{datetime.now()}] Error processing data: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return error_msg

if __name__ == "__main__":
    result = process_nutritional_data_from_azurite()
    print(result)
