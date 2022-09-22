# Dockerfile reference
# https://docs.docker.com/engine/reference/builder/#format

FROM gcc
RUN addgroup --gid 1000 appgroup
RUN useradd -r --uid 1000 -g appgroup appuser
RUN mkdir /home/appuser
RUN chown appuser:appgroup /home/appuser
COPY --chown=appuser:appgroup codi/* /home/appuser/
WORKDIR /home/appuser
USER appuser
RUN make
CMD ["./socket_server"]

