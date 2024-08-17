FROM python:3.10.11-bullseye

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "myapp.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]