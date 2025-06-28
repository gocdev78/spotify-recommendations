FROM python:3.11

WORKDIR /usr/src

COPY requirements_prod.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements_prod.txt

COPY . .

CMD ["streamlit", "run", "ui/app.py", "--server.port", "8000", "--server.runOnSave", "true"]