# Use the official Python Alpine image as the base image
FROM python:3.11-alpine

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
# RUN apk update \
#     && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# Set the working directory in the container
RUN mkdir /code
WORKDIR /code

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . /code/

# Expose the port on which the Django app will run
# EXPOSE 8000

# Set the command to run the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]