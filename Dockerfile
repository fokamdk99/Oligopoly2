# Use an official Python runtime as a base image
FROM python:3.7.4

# Set the working directory to /app
WORKDIR /oligopoly2

# Copy the current directory contents into the container at /app
ADD . /oligopoly2

# Install any needed packages
RUN pip install --upgrade pip && \
pip install pygame


# Run menu.py when the container launches
CMD ["python", "menu.py"]
