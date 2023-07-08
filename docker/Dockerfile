FROM python:3.8-slim
WORKDIR /app
ADD . /app
RUN apt-get update
RUN pip install -r requirements.txt

#ENV AWS_ACCESS_KEY_ID = ''

EXPOSE 8000
CMD ["python", "app.py", "extra_trees"]

