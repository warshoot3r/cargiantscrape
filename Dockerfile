FROM python:3.9-slim-bullseye
# Set up requirements for scraping
# Update the package lists and install required system packages
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt install -y python3 python3-dev virtualenv python3-venv
ENV _PYTHON_HOST_PLATFORM linux_armv7l
RUN pip3 install -U pip
# RUN pip3 install numpy --no-use-pep517
RUN pip3 install -v -r requirements.txt 

# Set up chrome selenium
RUN apt-get update && apt-get install -y \
    unzip \
    chromium \
    chromium-driver

# Copy class files and main.py
COPY modules .
COPY main.py .
# set ENV
ENV PATH="/usr/lib/chromium-browser/:${PATH}"
ENV CHROME_DRIVER=/usr/lib/chromium-browser/chromedriver
ENV CHROME_OPTIONS="--headless"

RUN pip3 install pandas -v
CMD [ "python", "main.py" ]