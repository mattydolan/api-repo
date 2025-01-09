# Use an official Python runtime as the base image
FROM python:3.12.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Python script
CMD ["python", "matt.py"]
