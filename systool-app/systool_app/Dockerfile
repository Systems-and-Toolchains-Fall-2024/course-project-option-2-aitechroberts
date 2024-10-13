# Use the official Python 3.10 Alpine image
FROM python:3.10-slim

# Install system dependencies
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    cargo \
    git \
    bash

# Install Poetry
RUN pip install --no-cache poetry

# Set the working directory
WORKDIR /app

# Copy only the pyproject.toml and poetry.lock files first
COPY pyproject.toml poetry.lock ./

# Install the dependencies using Poetry
RUN poetry install --no-root --no-dev

# Copy Home and the MPA Pages
COPY app.py app.py
# COPY ./pages ./pages

# Expose the port that Streamlit runs on
EXPOSE 8501

# Run the Streamlit app
ENTRYPOINT ["poetry", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]