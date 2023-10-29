# Use the official Ubuntu image as the base image
FROM ubuntu

# Set non-interactive mode during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and upgrade the system packages
RUN apt-get update && apt-get upgrade -y

# Install required dependencies
RUN apt-get install -y curl wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev software-properties-common


# Install libpq-dev
RUN apt-get install -y libpq-dev

# Add the deadsnakes PPA for Python 3.11
RUN add-apt-repository ppa:deadsnakes/ppa

# Install Python 3.11.3
RUN apt-get update && apt-get install -y python3.11

# Install pip
RUN apt-get install -y python3-pip

# Install Django
RUN apt-get install -y python3-django

# Install system packages required for Pillow
RUN apt-get install -y libjpeg-dev zlib1g-dev libtiff-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

# Create a working directory and set it as the working directory
WORKDIR /app

# Copy your Django project source code to the container
COPY . /app
# Change to the directory where the Django project is located
WORKDIR /app/Django-2021-master
# Install project requirements
RUN pip install -r requirements.txt

# Perform database migrations
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# Expose the Django development server's port
EXPOSE 8000

# Start the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
