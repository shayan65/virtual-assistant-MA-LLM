FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY . .

# Install the package using setup.py
RUN pip install -e .

# Upgrade pip and Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install gunicorn and uvicorn
RUN pip install gunicorn uvicorn

# Set the environment variable
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Expose the necessary ports
EXPOSE 8000

# Run the application with Gunicorn and 4 Uvicorn workers
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "agents.main:app", "--bind", "0.0.0.0:8000"]
