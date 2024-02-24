FROM python:slim

WORKDIR script_db

COPY requirements.txt ./requirements.txt

COPY ./config ./credentials /root/.aws/

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./database_init.py ./database_init.py

CMD ["python", "database_init.py"]
