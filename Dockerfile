FROM python:3.9-slim

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

ENV DEBUG="True"


RUN pip install --upgrade pip


COPY req.txt .
COPY . .
RUN chmod +x bot.py
RUN pip install -r req.txt

ARG CACHEBUST=1

CMD  python3 bot.py