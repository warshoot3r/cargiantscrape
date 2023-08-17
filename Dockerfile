# Use a smaller base image
FROM --platform=$BUILDPLATFORM python:3.9-slim AS base

# Set up requirements for scraping
WORKDIR /app
COPY requirements.txt .
ENV _PYTHON_HOST_PLATFORM linux_armv7l

# Install the other dependencies from requirements.txt
RUN pip3 install -r requirements.txt --no-build-isolation

# Set up chrome selenium
RUN apt-get update && apt-get install -y \
    unzip \
    chromium \
    chromium-driver

# Final runtime image
FROM base AS final

# Set ENV
ENV PATH="/usr/lib/chromium-browser/:${PATH}"
ENV CHROME_DRIVER=/usr/lib/chromium-browser/chromedriver
ENV CHROME_OPTIONS="--headless"

# Copy class files and main.py
COPY modules .
COPY chatbot_autorun.py .
COPY remove_unresolvable_cars.py .
COPY test.py .

CMD [ "python", "chatbot_autorun.py" ] 
