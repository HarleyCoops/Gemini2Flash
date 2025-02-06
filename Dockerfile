FROM vllm/vllm-openai

# Copy the application code
COPY vllm_inference.py /app/

# Expose the port
EXPOSE 8000

# Command to run the vLLM server (already running in the base image)
#CMD ["vllm", "serve", "HarleyCooper/GRPOtuned", "--host", "0.0.0.0"]
