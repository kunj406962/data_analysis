# Cloud-Native Nutritional Insights Application

A cloud-native data processing application that analyzes dietary datasets, containerizes the processing logic using Docker, and simulates serverless execution using Azurite and Azure Functions.

---

## Project Overview

This project processes a dataset of diet recipes (`All_Diets.csv`) to generate nutritional insights, including:

- Average macronutrients per diet type
- Top 5 protein-rich recipes per diet
- Macronutrient ratio calculations
- Data visualizations
- Containerized execution using Docker
- Simulated serverless processing using Azure Functions

The goal is to demonstrate **cloud-native application development concepts locally** without using live Azure resources.

---

## Technologies Used

- Python
- Pandas
- Matplotlib
- Seaborn
- Docker
- Docker Compose
- Azure Functions (local runtime)
- Azurite Blob Storage Emulator

---

## Task 1 — Data Processing

The script `data_analysis.py` performs:

- Dataset loading
- Missing value handling
- Grouping and aggregation
- Derived metric calculations
- Visualization generation

Example output files:

- `avg_macros.csv`
- `top_protein.csv`
- `nosql_output.json`

Run locally:

```bash
pip install -r requirements.txt
python data_analysis.py
```

---

## Task 2 — Docker Containerization

### Build Image

```bash
docker build -t diet-analysis .
```

### Run Container

```bash
docker run -it diet-analysis
```

---

## Docker Hub Image

Add your Docker Hub image link below:

```
https://hub.docker.com/r/pkunjj/diet-analysis
```

Pull and run:

```bash
docker pull pkunjj/diet-analysis
docker run -it pkunjj/diet-analysis
```

---

## Docker Compose Deployment Simulation

Run:

```bash
docker compose up
```

This simulates container deployment locally.

---

## Task 3 — Serverless Simulation

The serverless workflow:

1. Upload CSV to Azurite Blob Storage
2. Azure Function (Blob Trigger) processes the dataset
3. Results saved as JSON (simulated NoSQL storage)

Run Azure Function locally:

```bash
func start
```

---

## Project Structure

```
project/
│
├── All_Diets.csv
├── data_analysis.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── diet-function-app/
```

---

## Deliverables

- Dockerfile
- Docker image pushed to Docker Hub
- Docker Compose deployment simulation
- Azure Function execution using Azurite
- Generated data outputs

---

## Learning Outcomes

This project demonstrates:

- Data analysis with Pandas
- Docker containerization
- Container registry workflows
- Serverless computing concepts
- Local cloud service emulation...
