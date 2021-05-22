FROM tiangolo/uvicorn-gunicorn:python3.8

RUN pip install --upgrade pip

RUN pip uninstall uvicorn -y

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 80