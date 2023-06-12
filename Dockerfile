# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

# Add the app directory contents into the container at /app
ADD ./app /app

# Go up one level and install any needed packages specified in requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r ./requirements.txt

# Make $PORT available for the app
#ARG PORT
#EXPOSE $PORT

# Run app.py when the container launches
CMD ["python", "app.py"]