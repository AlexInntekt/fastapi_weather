FROM python:3.8-slim


COPY . /app

RUN pip install uvicorn
RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

WORKDIR /app

RUN pipenv install --deploy --system

EXPOSE 80

CMD ["ls"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]