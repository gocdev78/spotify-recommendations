FROM python:3.11

WORKDIR /usr/src

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["bash"]