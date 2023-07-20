FROM python:3.9

WORKDIR /app


# Set up requirements for python
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY ../modules /app/
COPY ../main.py /app/

CMD [ "python", "main.py" ]
