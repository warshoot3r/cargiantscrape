# syntax=docker/dockerfile:1.4

# Stage 1: Install Python packages
FROM python:3.9-slim-bookworm AS pythonpackages
COPY requirements.txt .

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

RUN pip install --prefer-binary --extra-index-url https://www.piwheels.org/simple -r requirements.txt



from python:3.9-slim-bookworm as final
COPY --from=pythonpackages /app/venv ./venv
ENV PATH="/app/venv/bin:$PATH"
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    libatlas3-base libgfortran5 

#Set env
ENV PATH="/usr/lib/chromium/:$PATH"
ENV CHROME_DRIVER=/usr/bin/chromedriver

workdir /app
# Copy class files and main.py
COPY modules /app/modules
COPY remove_unresolvable_cars.py .
COPY chatbot_autorun.py .
COPY test.py .

ENTRYPOINT ["python3"]
CMD ["chatbot_autorun.py"] 
