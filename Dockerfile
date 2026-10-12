FROM python:3.11-alpine
WORKDIR /app
COPY OPP3.py /app/TestDF.py
ENTRYPOINT ["python", "TestDF.py"]