FROM python:3.9.0-slim-buster
WORKDIR /app
COPY . .
RUN pip install pipenv
RUN pipenv install
CMD ["pipenv", "run", "start"]
EXPOSE 4040
