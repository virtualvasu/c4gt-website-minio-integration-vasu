# Contributing to C4GT Website

This document provides detailed guidelines on how to set up and run the C4GT website using Docker.

## Table of Contents

- [Setup Using Docker](#setup-using-docker)
- [Dockerfile Details](#dockerfile-details)
- [Docker Compose Details](#docker-compose-details)
- [Development Workflow](#development-workflow)
- [Troubleshooting](#troubleshooting)

## Setup Using Docker

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system
- [Docker Compose](https://docs.docker.com/compose/install/) installed on your system
- Git installed on your system

### Steps to Set Up

1. **Clone the repository**

    ```bash
    git clone https://github.com/your-repo/c4gt-website.git
    cd c4gt-website
    ```

2. **Create an environment file**

    Create a `.env` file in the root directory with the variables defined in `.env.example`:

    ```bash
    cp .env.example .env
    ```

3. **Build and start the containers**

    ```bash
    docker-compose up --build
    ```

    This will build the application image and start both the application and database containers in detached mode.

4. **Verify the setup**

    Access the website at `http://localhost:5000`

    You can check the status of your containers with:
    ```bash
    docker-compose ps
    ```

5. **Stop the containers**

    ```bash
    docker-compose down
    ```

## Dockerfile Details

Our Dockerfile implements a multi-stage build process to create an optimized, secure container.

### Builder Stage

```dockerfile
FROM python:3.9-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
     build-essential \
     && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

- Uses `python:3.9-slim` as the base image to reduce size
- Sets `/app` as the working directory
- Installs minimal build dependencies required for compiling Python packages
- Installs Python dependencies from requirements.txt

### Production Stage

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
     libgomp1 \
     && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
```

- Starts fresh with a clean `python:3.9-slim` image
- Installs only the runtime dependencies needed
- Copies the pre-built Python packages from the builder stage

### Security Features
- Exposes port 5000 for the application
- Implements a health check to ensure the application is running properly
- Sets the default command to start the application

## Docker Compose Details

The `docker-compose.yaml` file defines and configures the services needed for the application.

### Database Service
- Uses MySQL 8.0
- Configures database credentials using environment variables
- Persists data using a named volume
- Exposes port 3306 for database connections
- Includes a health check to ensure the database is running
- Connects to a custom network for service communication

### Application Service
- Builds the application using the local Dockerfile
- Loads environment variables from the .env file
- Sets the database host to the service name
- Exposes port 5000 for accessing the web application
- Ensures the database service is started first
- Includes a health check to verify the application is responding

### Networks and Volumes
- Creates a bridge network for service communication
- Defines a persistent volume for database data

## Development Workflow

1. Make changes to your code locally
2. Rebuild and restart the containers:
    ```bash
    docker-compose down
    docker-compose up --build -d
    ```
3. View logs to check for errors:
    ```bash
    docker-compose logs -f
    ```

## Troubleshooting

- **Database connection issues**: Ensure the environment variables are correctly set and that the database has fully started before the app attempts to connect.
- **Permission issues**: Check that the application user has correct permissions on all required files.
- **Port conflicts**: Ensure ports 5000 and 3306 are not being used by other services on your machine.

## Detailed breakdown

> There is a blog, dedicated to explain the functionalities and details of the file in her: [medium blog](https://medium.com/@rohansen856/docker-101-containerizing-the-c4gt-website-5a208000f2e6)