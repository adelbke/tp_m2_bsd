FROM python:3-alpine

# RUN addgroup -S -h pythongroup && adduser -S pythonuser -G pythongroup

COPY . /app

# USER pythonuser
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install flask
# RUN pip install flask && \
#     pip install -U Flask-WTF

CMD ["flask", "run", "--host" ,"0.0.0.0"]