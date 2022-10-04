#FROM buildpack-deps:bullseye-curl
FROM gcc

WORKDIR /home/appuser/practica4

RUN addgroup --gid 1000 appgroup
RUN useradd -r --uid 1000 -g appgroup appuser
RUN mkdir -p /home/appuser/practica4
RUN chown appuser:appgroup /home/appuser/practica4

COPY --chown=appuser:appgroup ./ /home/appuser/practica4

USER appuser