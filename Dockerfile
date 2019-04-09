# Base image to get from dockerhub
FROM alpine:latest

# Install python 3 and pip to the base image 
RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

#Install dependencies for Numpy and Pillow
RUN apk add --no-cache --update curl gcc g++ libxslt-dev
RUN apk --update add libxml2-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
# Define the working directory for the container
WORKDIR /app

# Copy files from the current directory into the /app directory
COPY . /app

# Install requirements fot the project
RUN pip3 --no-cache-dir install -r requirements.txt

# Open a port to allow connection to the container
EXPOSE 4000

# Define the command to be run on startup
ENTRYPOINT [ "python3" ]
CMD [ "api.py" ]