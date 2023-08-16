# Use a smaller base image
FROM python:3.9-slim-bullseye AS base

# Set up requirements for scraping
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

COPY requirements.txt .
# Install dependencies and set ENV
RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r requirements.txt

# Set ENV
ENV PATH="/usr/lib/chromium-browser/:${PATH}"
ENV CHROME_DRIVER=/usr/lib/chromium-browser/chromedriver
ENV CHROME_OPTIONS="--headless"

# Copy only necessary files
COPY modules /app/modules
COPY chatbot_autorun.py .
COPY test.py .

# Set the command to run
CMD [ "python", "chatbot_autorun.py" ]