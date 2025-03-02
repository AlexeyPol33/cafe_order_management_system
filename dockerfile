FROM python:3.8.10
ENV DEBUG 0
ENV  DB_ENGINE django.db.backends.postgresql
ENV  DB_NAME postgres_basic
ENV  DB_USER postgres
ENV  DB_PASSWORD postgres
ENV  DB_HOST postgredb
ENV  DB_PORT 5432

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/CafeOrderSystem

RUN python manage.py migrate

#Подготовленные тест данные, для ознакомительного просмотра
RUN python manage.py load_meals --file=../TestData/meals.yaml

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]