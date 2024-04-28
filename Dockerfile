FROM python:3.12

# Set working directory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Gunicorn will listen on
EXPOSE 8050

# Command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]
