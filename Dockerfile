# Use the official Python 3.8 slim image from Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the .py file when the container starts
CMD ["python", "dl_final_lab_exam_(aman_kumar_sinha).py"]

