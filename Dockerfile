FROM python:3.12

WORKDIR /app



RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8001"]
