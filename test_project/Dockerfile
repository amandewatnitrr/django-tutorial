# Use the official Python image as the base image
FROM python:3.11.3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Create a non-root user with an arbitrary UID (10014 is used here)
# Comment when not in use [Only used for Choreo]
RUN useradd -m -u 10001 appuser

# Switch to the non-root user
# Comment when not in use [Only used for Choreo]
USER 10001

# Copy the requirements.txt file to the working directory
COPY ./test_project/requirement_overall.txt .

# Install dependencies
RUN pip install -r requirement_overall.txt

# Copy the current directory into the working directory
COPY . .

# Expose the port that Django runs on
EXPOSE 8000

# Set the command to start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

