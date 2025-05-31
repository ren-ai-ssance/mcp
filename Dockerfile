FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unzip \
    build-essential \
    gcc \
    python3-dev \
    graphviz \
    graphviz-dev \
    pkg-config \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && npm install -g playwright \
    && npx playwright install chrome \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf aws awscliv2.zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*    

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir sarif-om==1.0.4
RUN pip install --no-cache-dir diagrams
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p .streamlit
COPY config.toml .streamlit/
COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "application/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
