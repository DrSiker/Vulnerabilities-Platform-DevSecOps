FROM postgres
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=password123
ENV POSTGRES_DB=vulndb
COPY init.sql /docker-entrypoint-initdb.d/
EXPOSE 5432