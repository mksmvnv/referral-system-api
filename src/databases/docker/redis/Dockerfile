FROM redis:latest

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

HEALTHCHECK --interval=10s --timeout=5s --retries=5 CMD redis-cli -a "$REDIS_PASSWORD" ping || exit 1

CMD ["/usr/local/bin/entrypoint.sh"]

