FROM python:slim

WORKDIR /fastapi

COPY requirements.txt ./requirements.txt

COPY database/config database/credentials /root/.aws/

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./app ./app

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
