FROM apache/airflow:3.1.8-python3.11

# Install our Python dependencies on top of the official image
# We do this in the Dockerfile rather than at runtime so the image
# is self-contained and reproducible
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
