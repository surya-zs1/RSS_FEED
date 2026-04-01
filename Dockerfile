# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bot's code
COPY . .

# Expose port 8080 (standard for most free web services)
EXPOSE 8080

# Command to run the bot
CMD ["python", "main.py"]