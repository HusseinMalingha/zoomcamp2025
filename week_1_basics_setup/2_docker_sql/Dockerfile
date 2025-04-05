FROM python:3.12

# Combine RUN commands and install correct packages
RUN apt-get update && \
    apt-get install -y wget gzip && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install pandas sqlalchemy psycopg2  

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]
