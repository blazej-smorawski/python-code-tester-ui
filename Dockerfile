FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY app.py /app/app.py
COPY edit.py /app/edit.py
COPY mainenance.py /app/mainenance.py
COPY src/* /app/src/
COPY src/blogs/* /app/src/blogs/
COPY requirements.txt /app/requirements.txt
COPY utils/* /app/utils/
COPY static/* /app/static/
COPY docs/* /app/docs/

RUN pip3 install -r requirements.txt

COPY index.html /usr/local/lib/python3.9/site-packages/streamlit/static/index.html
COPY favicon.png /usr/local/lib/python3.9/site-packages/streamlit/static/favicon.png

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run"]