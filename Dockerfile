# Define the base image
FROM python:3.11

# Define the working directory
WORKDIR /app

# Copy the necessary files to the container
COPY requirements.txt .
COPY .env .
COPY main.py .
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which Uvicorn will run
EXPOSE 8080

# Command to keep the container running. Services will be started by docker-compose
CMD ["sleep", "infinity"]
