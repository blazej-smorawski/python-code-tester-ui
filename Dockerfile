FROM nikolaik/python-nodejs:python3.11-nodejs18-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY test-code.py /app/test-code.py
COPY edit-view.py /app/edit-view.py
COPY requirements.txt /app/requirements.txt
COPY build_deps.sh /app/build_deps.sh
COPY utils/* /app/utils/
COPY deps/ /app/deps/
COPY static/* /app/static/
COPY docs/* /app/docs/

RUN pip3 install -r requirements.txt
RUN ./build_deps.sh

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run"]