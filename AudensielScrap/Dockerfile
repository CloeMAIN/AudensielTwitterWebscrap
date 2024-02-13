# Use Python 3.8 slim version as base image
FROM python:3.8-slim-buster

# Set working directory in the container
WORKDIR /AudensielTwitterWebscrap

# Copy requirements.txt and application code
COPY AudensielScrap/requirements.txt .
COPY AudensielScrap/ .

# Install necessary packages for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y wget gnupg

# Add Google Chrome repository key
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Add Google Chrome repository to the sources list
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update package lists and install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# Install unzip command
RUN apt-get install -y unzip



# Install ChromeDriver (replace '121.0.6167.85' with the appropriate version)
RUN wget -q -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/121.0.6167.85/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/bin && \
    rm /tmp/chromedriver.zip



# Install Django and other Python dependencies
RUN pip install -r requirements.txt


# Expose port 8000 for Django app
EXPOSE 8000

# Define the command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
