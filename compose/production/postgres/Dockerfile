<<<<<<< HEAD
FROM postgres:11
=======
FROM postgres:10
>>>>>>> 64408d580965fa7a0c7cafb79fdbe26e98c1dac2

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
