FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install flask reportlab

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
