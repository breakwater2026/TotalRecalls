# TotalRecalls marketing site — Cloud Run
# Build type: Dockerfile
# Dead-simple static file server (no nginx listen/IPv6/HTTP2 quirks)

FROM python:3.12-alpine

ENV PORT=8080 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv
COPY site/ /srv/

# Non-root
RUN adduser -D -u 10001 web \
    && chown -R web:web /srv
USER web

EXPOSE 8080

# Cloud Run injects PORT; bind all interfaces
CMD ["sh", "-c", "echo \"TotalRecalls static site on 0.0.0.0:${PORT}\" && exec python -m http.server \"${PORT}\" --bind 0.0.0.0"]
