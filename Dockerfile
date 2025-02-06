FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY vllm_inference.py .

# Expose the port
EXPOSE 8000

# Command to run the vLLM server
CMD ["vllm", "serve", "HarleyCooper/GRPOtuned", "--host", "0.0.0.0"]
