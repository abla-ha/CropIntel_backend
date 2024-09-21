# Use the official Ubuntu image as the base image
FROM ubuntu:latest

# Set environment variables to prevent some issues during installation
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    ca-certificates \
    curl \
    wget \
    vim \
    nano \
    git \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate the virtual environment and install Python packages
RUN /opt/venv/bin/pip install --upgrade pip

# Add the virtual environment to PATH
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install -r requirements.txt

CMD [ "uvicorn main:app --reload" ]

EXPOSE 8000