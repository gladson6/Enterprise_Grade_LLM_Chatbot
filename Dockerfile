# 1. Use an official, slim Python image as a base
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements file first to leverage Docker's layer caching
COPY functions/requirements.txt .

# 4. Install all Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# 5. THIS IS THE MISSING STEP: Copy the downloaded model into the container
COPY local_model/ ./local_model/

# 6. Copy your entire application code into the container.
COPY functions/ .

# 7. Command to run the application.
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1

