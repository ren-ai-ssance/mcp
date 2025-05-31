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
    terminator \
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

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

RUN pip install streamlit==1.41.0 streamlit-chat pandas numpy boto3
RUN pip install langchain_aws langchain langchain_community langgraph langchain_experimental
RUN pip install langgraph-supervisor langgraph-swarm
RUN pip install tavily-python==0.5.0 yfinance==0.2.52 rizaio==0.8.0 pytz==2024.2 beautifulsoup4==4.12.3
RUN pip install plotly_express==0.4.1 matplotlib==3.10.0
RUN pip install PyPDF2==3.0.1 opensearch-py
RUN pip install mcp langchain-mcp-adapters==0.0.9 wikipedia
RUN pip install aioboto3 requests uv kaleido diagrams
RUN pip install graphviz sarif-om==1.0.4

RUN mkdir -p .streamlit
COPY config.toml .streamlit/

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "application/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
