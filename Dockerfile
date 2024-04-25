# Use an official Ubuntu base image
FROM ubuntu:latest

# Set the environment variable to disable interactive frontend
ENV DEBIAN_FRONTEND=noninteractive

# Install PostgreSQL and required utilities
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    tzdata \
    locales

# Configure timezone and locales
RUN echo "UTC" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    locale-gen en_US.UTF-8

# Switch to the 'postgres' user to avoid using root
USER postgres

# Initialize the database and create the PostgreSQL user 'docker'
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" && \
    createdb -O docker docker

# Adjust PostgreSQL configuration to allow external connections
# Ensure the version number in the path matches the PostgreSQL version installed
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/14/main/pg_hba.conf && \
    echo "listen_addresses='*'" >> /etc/postgresql/14/main/postgresql.conf

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Set the default command to run when starting the container
CMD ["/usr/lib/postgresql/14/bin/postgres", "-D", "/var/lib/postgresql/14/main", "-c", "config_file=/etc/postgresql/14/main/postgresql.conf"]
