# Use a Python base image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies defined in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5001 (in MacOS, AirPlay uses ports 5000 and 7000!)
EXPOSE 5001

# Default command to run your application when the container starts
CMD ["python", "app/app.py"]