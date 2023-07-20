FROM python:3.9

WORKDIR /app


# Set up requirements for scraping
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



# Set up chrome selenium
RUN apt-get update && apt-get install -y \
    unzip \
    chromium-browser \
    chromium-chromedriver

# Copy class files and main.py
COPY modules .
COPY main.py .

# set ENV
ENV PATH="/usr/lib/chromium-browser/:${PATH}"
ENV CHROME_DRIVER=/usr/lib/chromium-browser/chromedriver
ENV CHROME_OPTIONS="--headless"

CMD [ "python", "main.py" ]
