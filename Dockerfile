FROM python:3.9-slim

# Set the working directory
WORKDIR /

# Copy server files into the container
COPY . .

# Expose the port the server listens on
EXPOSE 3000

# Run the server
CMD ["python", "server.py"]