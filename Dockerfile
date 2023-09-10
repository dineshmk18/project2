FROM python:3.11

WORKDIR /app


RUN pip install Flask
RUN pip install gunicorn
RUN pip install SQLAlchemy
RUN pip install flask_sqlalchemy
RUN pip install mysql-connector-python gunicorn
RUN pip install azure.identity
RUN pip install azure.keyvault.secrets

COPY . .

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80"]
