# Use the official Python image as the base image
FROM python:3.8.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y poppler-utils

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-eng


ENV AWS_ACCESS_KEY_ID="AKIA2G47Q5KBUZ3B5C2M"
ENV AWS_SECRET_ACCESS_KEY="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"
ENV AWS_DEFAULT_REGION="us-east-1"


# Copy the application code to the working directory
COPY . .

# Expose the port that the Flask application will be running on
EXPOSE 5000 443

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]