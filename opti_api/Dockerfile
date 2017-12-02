# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app/requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt \
&& rm /app/requirements.txt


# Make port 5000 available to the world outside this container

# Define environment variable
ENV Name JWT_SECRET_KEY
ENV Name MYSQL_HOST
ENV Name MYSQL_USER
ENV Name MYSQL_PASSWORD
ENV Name MYSQL_DB
ENV Name DEBUG

COPY ./app/app.py /app

# Run app.py when the container launches
CMD ["python", "app.py"]
