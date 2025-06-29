FROM python:3
RUN pip install diagrams
RUN apt-get update && apt-get install -y \
    graphviz \
 && rm -rf /var/lib/apt/lists/*
RUN mkdir src
WORKDIR /src/
CMD [ "python", "homelab.py" ]