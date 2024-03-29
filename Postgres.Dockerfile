FROM ankane/pgvector:latest

# Set the locale and collation settings
RUN localedef -i en_US -f UTF-8 en_US.UTF-8
ENV LC_COLLATE=en_US.UTF-8
ENV LC_CTYPE=en_US.UTF-8

CMD ["postgres"]
