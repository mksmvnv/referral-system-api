FROM postgres:16

HEALTHCHECK --interval=10s --timeout=5s --retries=5 CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1

VOLUME /var/lib/postgresql/data
