FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
WORKDIR /app
ENV PYTHONPATH=/app/app
COPY ./worker-start.sh /worker-start.sh
RUN chmod +x /worker-start.sh
CMD ["bash", "/worker-start.sh"]