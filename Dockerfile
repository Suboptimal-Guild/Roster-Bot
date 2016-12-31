FROM jfloff/alpine-python:latest-slim

# Copy harambot files in
COPY /run.py /run.py
COPY /google /google
COPY /commands /commands

# Copy requirements file for package installation.
COPY /requirements.txt /requirements.txt

# Copy the credentials files
COPY .credentials /root/.credentials

# Add all of the python packages we need.
RUN pip install -r requirements.txt
