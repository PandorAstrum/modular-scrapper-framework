# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install Twisted wheel Before To prevent C++ build tools look up
RUN pip install Twisted-19.2.0-cp36-cp36m-win_amd64.whl

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run scrapy server mutithreaded job system
RUN scrapyd

# Create egg of spiders and deploy to Server
RUN scrapyd-deploy local
