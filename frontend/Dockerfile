FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir flask requests gunicorn
EXPOSE 3000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "app:app"]
