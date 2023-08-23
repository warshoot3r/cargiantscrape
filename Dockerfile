# syntax=docker/dockerfile:1.4

# Stage 1: Install Python packages
FROM python:3.11.4-slim-bullseye@sha256:40319d0a897896e746edf877783ef39685d44e90e1e6de8d964d0382df0d4952 AS pythonpackages
COPY --link requirements.txt .

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:${PATH}"
RUN pip install --prefer-binary --extra-index-url https://www.piwheels.org/simple -r requirements.txt



from python:3.11.4-slim-bullseye as final
workdir /app
COPY --link --from=pythonpackages /app/venv ./venv
ENV PATH="/app/venv/bin:${PATH}"
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    libatlas3-base libgfortran5 

#Set env
ENV PATH="/usr/lib/chromium/:${PATH}"
ENV CHROME_DRIVER=/usr/bin/chromedriver

# Copy class files and main.py
COPY --link modules /app/modules
COPY --link remove_unresolvable_cars.py .
COPY --link chatbot_autorun.py .
COPY --link test.py .

ENTRYPOINT ["python3"]
CMD ["chatbot_autorun.py"] 
