# Image for a Python 3 development environment
FROM python:3.9-slim

# Add any tools that are needed beyond Python 3
RUN apt-get update && \
    apt-get install -y sudo vim make git zip tree curl wget jq unzip gnupg && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    # Chromedriver installation and setup
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver

# Create a user for development
ARG USERNAME=devops
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user with passwordless sudo privileges
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && usermod -aG sudo $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Added libraries for PostgreSQL
RUN apt-get install -y gcc libpq-dev

# Set up the Python development environment
WORKDIR /app
RUN python -m pip install --upgrade pip wheel

EXPOSE 8080

# Enable color terminal for docker exec bash
ENV TERM=xterm-256color

# Become a regular user
USER $USERNAME