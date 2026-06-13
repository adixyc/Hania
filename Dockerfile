# Use a lightweight and official Python image
FROM python:3.11-slim

# Set a secure working directory inside the container
WORKDIR /app

# Copy the requirements file first to take advantage of Docker caching
COPY requirements.txt .

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bot's source code into the container
COPY . .

# Run your main script (assuming your file is named main.py)
CMD ["python", "main.py"]
