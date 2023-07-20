FROM python:3.9

WORKDIR /app


# Set up requirements for python
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY modules .
COPY main.py .

CMD [ "python", "main.py" ]
