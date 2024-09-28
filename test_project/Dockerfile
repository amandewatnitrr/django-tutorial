# Use the official Python image as the base image
FROM python:3.11.3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Create a non-root user with a UID between 10000 and 20000 (e.g., 10001)
RUN useradd -m -u 10001 appuser

# Switch to the non-root user
USER 10001

# Copy the requirements.txt file to the working directory
COPY ./requirement_overall.txt .

# Install dependencies (use the --user flag to avoid permission issues)
RUN pip install --user -r requirement_overall.txt

# Copy the current directory into the working directory
COPY . .

# Expose the port that Django runs on
EXPOSE 8000

# Set the command to start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
