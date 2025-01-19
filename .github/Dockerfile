# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright dependencies
RUN apt-get update && apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libxcomposite1 libxrandr2 libxdamage1 libxkbcommon0 libasound2 libpangocairo-1.0-0 libpango-1.0-0 libcups2 libnss3 libxshmfence1 libgbm1 libgtk-3-0

# Install Playwright browsers
RUN playwright install

# Copy the rest of the app's code
COPY . /app/

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
