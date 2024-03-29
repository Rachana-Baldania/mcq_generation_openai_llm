FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
WORKDIR /app
ENV PYTHONPATH=/app/app
COPY ./beat-start.sh /beat-start.sh
RUN chmod +x /beat-start.sh
CMD ["bash", "/beat-start.sh"]