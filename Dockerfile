FROM python:3.7
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN alembic init migrations && cp env.py ./migrations/
