# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install all the necessary Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files into the container
COPY . .

# Tell Docker that your app will run on port 5000
EXPOSE 5000

# The command to run your Flask app when the container starts
CMD ["python", "app.py"]