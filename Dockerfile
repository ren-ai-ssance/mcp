FROM python:3.12-slim

WORKDIR /app

# .env 파일을 복사
COPY .env .env

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# .streamlit 설정 파일 복사
COPY .streamlit .streamlit

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "application/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
