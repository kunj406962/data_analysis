# Use an official Python runtime as a parent image
# (slim version to reduce image size and improve effeiciency)
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the dependencies file to the container
COPY requirements.txt .

# Install only required python packages to reduce image size and improve efficiency
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Allows matplotlib to work without a display (useful for headless environments like Docker)
ENV MPLBACKEND=Agg

CMD ["python", "data_analysis.py"]