ARG AIRFLOW_VERSION=2.9.2
ARG PYTHON_VERSION=3.10


# Use the official Airflow image as the base image
FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

# Set the Airflow home directory for the container which will contain DAGs, logs, and other configurations
ENV AIRFLOW_HOME=/opt/airflow


# define the extra packages to be installed that are required for the project
COPY requirements.txt .

# Install the required packages
RUN pip install -no-cache-dir "apache_ariflow==${AIRFLOW_VERSION}" -r /requirements.txt