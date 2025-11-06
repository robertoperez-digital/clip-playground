FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt


COPY . /code/

EXPOSE 3050

CMD ["fastapi", "run", "main.py", "--port", "8000"]