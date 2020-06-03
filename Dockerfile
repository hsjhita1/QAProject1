FROM python:latest
WORKDIR /opt/QAProject1
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]