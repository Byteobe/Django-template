# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.12.4
ENV PYTHONUNBUFFERED=1

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    postgis \
    gdal-bin \
    python3-gdal \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    gettext \
    wkhtmltopdf \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*

# Setup workdir
RUN mkdir /src
WORKDIR /src

# Copy the requirements file and install dependencies
COPY requirements.txt /src/
RUN pip install -r /src/requirements.txt
RUN pip install uvicorn[standard]


# Copy the rest of the application code
COPY . /src

# Give execute permission to manage.py and start.sh
RUN chmod +x /src/manage.py

# Use start.sh as the entry point
CMD ["/src/scripts/start.sh"]