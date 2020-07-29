FROM ubuntu:20.04

# install deps
RUN apt-get update \
    && apt-get install -y \
        python3 \
        curl \
        gcc
# install rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# create directories
RUN mkdir -p /build/src
RUN mkdir -p /var/www/images
RUN mkdir /var/data
# Move into build dir
WORKDIR /build
# Copy in build assets
COPY Cargo.toml /build/
COPY Cargo.lock /build/
COPY src /build/src

# Build and Move web server
RUN PATH=$PATH:~/.cargo/bin cargo build --release
RUN mv ./target/release/acnh_util /usr/local/bin/

# Setup ENV
ENV ACNH_DIR /var/www/
ENV ACNH_DATABASE /var/data/acnh.sqlite
ENV ACHN_PORT 80

# Seed DB
COPY seed.py /build/
RUN python3 ./seed.py

# Web assets
COPY ./public/*.html /var/www/
COPY ./public/*.js /var/www/
COPY ./public/*.css /var/www/
COPY ./public/images/* /var/www/images/

# Clean up
RUN rm -rf /build
RUN apt-get remove gcc python curl -y
RUN PATH=$PATH:~/.cargo/bin rustup self uninstall -y
WORKDIR /usr/local/bin/
ENTRYPOINT 'acnh_util'
