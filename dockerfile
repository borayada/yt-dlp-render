FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Copy app files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
