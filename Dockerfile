# Use a smaller base image
FROM python:3.9-slim-bullseye AS base

# Set up requirements for scraping
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3 python3-dev virtualenv python3-venv
ENV _PYTHON_HOST_PLATFORM linux_armv7l
RUN pip3 install -U pip
RUN pip3 install -v -r requirements.txt 

# Set up chrome selenium
RUN apt-get update && apt-get install -y \
    unzip \
    chromium \
    chromium-driver

# Final runtime image
FROM base AS final

# Install pandas
RUN pip3 install pandas -v

# Set ENV
ENV PATH="/usr/lib/chromium-browser/:${PATH}"
ENV CHROME_DRIVER=/usr/lib/chromium-browser/chromedriver
ENV CHROME_OPTIONS="--headless"

# Copy class files and main.py
COPY modules /app/modules
COPY chatbot_autorun.py .
COPY remove_unresolvable_cars.py .
COPY test.py .

CMD [ "python", "chatbot_autorun.py" ]