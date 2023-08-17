# Use a smaller base image
FROM --platform=$BUILDPLATFORM python:3.9-slim AS base

# Set up requirements for scraping
WORKDIR /app
COPY requirements.txt .
# Automatically determine the platform and set the environment variable
ENV ARCH="$(dpkg --print-architecture)"
ENV _PYTHON_HOST_PLATFORM=${ARCH}

RUN echo "Setting _PYTHON_HOST_PLATFORM to ${_PYTHON_HOST_PLATFORM}" && \
    echo "export _PYTHON_HOST_PLATFORM=${_PYTHON_HOST_PLATFORM}" >> /etc/environment

# Install the other dependencies from requirements.txt
RUN pip3 install --only-binary :all: -r requirements.txt

# Set up chrome selenium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver

# Final runtime image
FROM base AS final

# Set ENV
ENV PATH="/usr/lib/chromium-browser/:${PATH}"
ENV CHROME_DRIVER=/usr/lib/chromium-browser/chromedriver
ENV CHROME_OPTIONS="--headless"

# Copy class files and main.py
COPY modules /app/modules
COPY chatbot_autorun.py .
COPY remove_unresolvable_cars.py .
COPY test.py .
# Make scripts executable 
RUN chmod +x *.py 
CMD [ "python", "chatbot_autorun.py" ] 
