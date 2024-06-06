FROM nvidia/cuda:12.0.0-runtime-ubuntu22.04



RUN apt-get update && apt upgrade -y && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip libcudnn8 libcudnn8-dev \
    && rm -rf /var/lib/apt/lists/*

  
RUN python3 -m pip install --upgrade pip

WORKDIR /app
COPY main.py ./
COPY server.py ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "server.py" ]